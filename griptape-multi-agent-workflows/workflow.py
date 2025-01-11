import os

from griptape.drivers import (
    GriptapeCloudStructureRunDriver,
    GriptapeCloudEventListenerDriver,
)
from griptape.structures import Workflow
from griptape.tasks import PromptTask, StructureRunTask
from griptape.events import EventBus, EventListener

WRITERS = [
    {
        "role": "Travel Adventure Blogger",
        "goal": "Inspire wanderlust with stories of hidden gems and exotic locales",
        "backstory": "With a passport full of stamps, you bring distant cultures and breathtaking scenes to life through vivid storytelling and personal anecdotes.",
    },
    {
        "role": "Lifestyle Freelance Writer",
        "goal": "Share practical advice on living a balanced and stylish life",
        "backstory": "From the latest trends in home decor to tips for wellness, your articles help readers create a life that feels both aspirational and attainable.",
    },
]

def get_listener_api_key() -> str:
    api_key = os.environ.get("GT_CLOUD_API_KEY", "")
    if not api_key:
        print(
            """
              ****WARNING****: No value was found for the 'GT_CLOUD_API_KEY' environment variable.
              This environment variable is required when running in Griptape Cloud for authorization.
              You can generate a Griptape Cloud API Key by visiting https://cloud.griptape.ai/keys .
              Specify it as an environment variable when creating a Managed Structure in Griptape Cloud.
              """
        )
    return api_key

if __name__ == "__main__":
    # Set up the EventBus
    EventBus.add_event_listener(
        EventListener(
            event_listener_driver=GriptapeCloudEventListenerDriver(
                api_key=get_listener_api_key()
            )
        )
    )

    # Build the team
    team = Workflow()
    research_task = team.add_task(
        StructureRunTask(
            (
                """Perform a detailed examination of the newest developments in AI as of 2024.
                Pinpoint major trends, breakthroughs, and their implications for various industries.""",
            ),
            id="research",
            structure_run_driver=GriptapeCloudStructureRunDriver(
                api_key=os.environ["GT_CLOUD_API_KEY"],
                structure_id=os.environ["GT_RESEARCH_STRUCTURE_ID"],
                structure_run_max_wait_time_attempts=30 # takes 50 seconds to run
            ),
        ),
    )
    end_task = team.add_task(
        PromptTask(
            'State "All Done!"',
        )
    )
    team.insert_tasks(
        research_task,
        [
            StructureRunTask(
                (
                    writer["role"],
                    writer["goal"],
                    writer["backstory"],
                    """Using insights provided, develop an engaging blog
                post that highlights the most significant AI advancements.
                Your post should be informative yet accessible, catering to a tech-savvy audience.
                Make it sound cool, avoid complex words so it doesn't sound like AI.

                Insights:
                {{ parent_outputs["research"] }}""",
                ),
                structure_run_driver=GriptapeCloudStructureRunDriver(
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                    structure_id=os.environ["GT_WRITER_STRUCTURE_ID"],
                    async_run=True,
                ),
            )
            for writer in WRITERS
        ],
        end_task,
    )

    team.run()
