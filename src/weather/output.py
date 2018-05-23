import json


def output_version() -> None:
    output = json.dumps(
        {
            "version":
            {
                "weather": "Really, you shouldn't be trying to change the weather, friend."
            }
        }
    )

    print(output)
