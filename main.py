from flask import Flask, redirect, render_template, request, url_for

from src.di.module import Container
from src.utils.ModerationException import ModerationException

app = Flask(__name__)

container = Container()
container.openai_config().load_openai_key()
application = container.application()


def initialize_conversation() -> str:
    initial_conversation = application.pipeline.run_stage0()

    return initial_conversation.response[0]


conversation = []
top_products = None
conversation.append({"assistant": initialize_conversation()})


@app.route("/")
def default_func():
    global conversation, top_products
    return render_template("index_invite.html", conversations=conversation)


@app.route("/end_conv", methods=["POST"])
def end_conv():
    global conversation, top_products
    conversation = []
    top_products = None
    application.pipeline.clear_messages()
    conversation.append({"assistant": initialize_conversation()})

    return redirect(url_for("default_func"))


@app.route("/invite", methods=["POST", "GET"])
def invite():
    global conversation, top_products
    user_input = request.form["user_input_message"]
    conversation.append({"user": user_input})

    try:
        if user_input == "exit":
            print("See you next time!. Please feel free to connect anytime!")
            return redirect(url_for("end_conv"))

        if top_products == None:
            stage1_response = application.pipeline.run_stage1(user_input=user_input)

            if stage1_response.intent_confirmation.strip().lower() == "yes":
                # stage 2
                stage_2_response = application.pipeline.run_stage2(
                    user_requirement=stage1_response.user_requirements
                )
                top_products = stage_2_response.recommendations
                if len(top_products) == 0:
                    conversation.append(
                        {
                            "assistant": "Sorry we do not have AC's that match your requirements. Connecting you to a human expert."
                        }
                    )

                # stage 3 initializing conversation
                stage3_response = application.pipeline.run_stage3(
                    recommendations=stage_2_response.recommendations
                )
                conversation.append({"assistant": "\n".join(stage3_response.response)})
            else:
                conversation.append({"assistant": stage1_response.response})

        else:
            # stage 3 continue conversation
            stage3_response = application.pipeline.continue_stage3(user_input)
            conversation.append({"assistant": stage3_response.response[0]})

    except ModerationException as te:
        print(te)
        conversation.append({"assistant": te.message})
        return redirect(url_for("end_conv"))
    except Exception as e:
        print(e)
        conversation.append({"assistant": e})
        return redirect(url_for("end_conv"))

    return redirect(url_for("default_func"))


def main():
    app.run()


if __name__ == "__main__":
    main()
