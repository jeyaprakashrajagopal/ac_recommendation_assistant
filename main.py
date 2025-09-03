import json

from flask import (Flask, Response, redirect, render_template, request,
                   stream_with_context, url_for)

from src.di.module import Container
from src.utils.ModerationException import ModerationException

app = Flask(__name__)
container = Container()
container.openai_config().load_openai_key()
application = container.application()


def initialize_conversation() -> str:
    # Run Initialize conversation
    initial_conversation = application.pipeline.run_stage0()
    return initial_conversation.response


conversation = []
top_products = None
conversation.append({"assistant": initialize_conversation()[0]})


@app.route("/")
def default_func():
    global conversation, top_products
    return render_template("index_chat.html", conversations=conversation)


@app.route("/end_conv", methods=["POST"])
def end_conv():
    global conversation, top_products
    conversation = []
    top_products = None
    application.pipeline.clear_messages()
    conversation.append({"assistant": initialize_conversation()[0]})
    return redirect(url_for("default_func"))


@app.route("/chat_stream", methods=["POST"])
def chat_stream():
    global conversation, top_products
    user_input = request.form["user_input_message"]
    conversation.append({"user": user_input})

    @stream_with_context
    def generate():
        global top_products

        def send(role, text, event="message"):
            payload = json.dumps({"role": role, "text": text})
            return f"event:{event}\ndata:{payload}\n\n"

        yield send("user", user_input)

        try:
            if top_products is None:
                # Run Stage 1
                stage1 = application.pipeline.run_stage1(user_input=user_input)

                if stage1.intent_confirmation.strip().lower() == "yes":
                    stage2 = application.pipeline.run_stage2(
                        user_requirement=stage1.user_requirements
                    )
                    conversation.append({"assistant": stage1.response})

                    # Handle empty recommendataions
                    if not stage2.recommendations:
                        yield send(
                            "assistant",
                            "Sorry we do not have AC's that match your requirements. Connecting you to a human expert.",
                        )
                        yield "event:end\ndata:{}\n\n"
                        return

                    # Run Stage 3 with an initial conversation
                    stage3_response = application.pipeline.run_stage3(
                        recommendations=stage2.recommendations
                    )

                    conversation.append(
                        {"assistant": "\n".join(stage3_response.response)}
                    )
                    top_products = stage2.recommendations
                    yield send("assistant", "\n".join(stage3_response.response))
                else:
                    conversation.append({"assistant": stage1.response})
                    yield send("assistant", stage1.response)
            else:
                # Continue running Stage 3 to resume helping the customer
                stage3_continue_response = application.pipeline.continue_stage3(
                    user_input
                )
                response = stage3_continue_response.response
                yield send("assistant", response)
                conversation.append({"assistant": response})

        except ModerationException as te:
            yield send("assistant", te.message)
            yield "event:block\ndata:{}\n\n"
            return
        except Exception as e:
            yield send("assistant", str(e))
            yield "event:block\ndata:{}\n\n"
            return

        # To finish the stream
        yield "event:end\ndata:{}\n\n"

    return Response(generate(), mimetype="text/event-stream")


def main():
    app.run(debug=True, threaded=True)


if __name__ == "__main__":
    main()
