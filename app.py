from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from openai import OpenAI
import os
import asyncio

try:
    from setup import api_key1
except ImportError:
    api_key1 = os.getenv("OPENAI_API_KEY")

model_options = ["gpt-4o",]

app_info = """
This app creates RevealJS slides in Quarto document using OpenAI's 
GPT-4o-mini model (by default). 
Enter the outline for your slides and your OpenAI API key to get started. 
You can get an API key by visting the 
OpenAI API [quickstart page](https://platform.openai.com/docs/quickstart/).
You can also select a different OpenAI model if needed. 
You will need [Quarto](https://quarto.org/) to render the document 
into a RevealJS presentation.
"""

quarto_templates = {
    "Quarto slides": """
        ---
        title: "Habits"
        author: "John Doe"
        format: revealjs
        ---

        # In the morning

        ## Getting up

        - Turn off alarm
        - Get out of bed

        ## Breakfast

        - Eat eggs
        - Drink coffee

        # In the evening
        """,
}

app_ui = ui.page_fluid(
    ui.layout_sidebar( 
        ui.sidebar(
            ui.input_password(
                id = "api_key", 
                label = "Enter your OpenAI API key:", 
                value=api_key1
            ),
            ui.input_select(
                id = "model", 
                label = "Select OpenAI model:", 
                choices = model_options, 
                selected = "gpt-4o-mini"
            ),
            ui.input_text_area("outline", "Enter your outline for your slides:"),
            ui.input_select(
                id = "selected_template", 
                label = "Select Quarto output type:",
                choices = list(quarto_templates.keys()),
                selected = "Quarto slides"
            ),
            ui.input_action_button("convert", "Convert to Quarto"),
            open="always",
        ),
        ui.panel_title("Quarto Slides Generator"),
        ui.strong(
            ui.em(
                """an app to generate Quarto slides based on an outline using OpenAI's GPT-4o model 
                """
            )
        ),
        ui.markdown(app_info),
        ui.download_button("download", "Download Quarto File"),
        ui.output_text_verbatim("quarto_output"),
    )
)

def server(input, output, session):
    quarto_content = reactive.Value("")
    llm_prompt = reactive.Value("")

    @reactive.Effect
    @reactive.event(input.convert)
    def _():
        api_key = input.api_key()
        
        if not api_key:
            ui.notification_show("Please enter your OpenAI API key.", type="error")
            return   
        
        template = quarto_templates[input.selected_template()]
        template_type = input.selected_template()
        outline = input.outline()

        llm_prompt.set([
            {"role": "system", 
            "content": f"""You are a highly proficient assistant tasked with 
            generating {template_type} content into a structured Quarto document.
            The goal is to create a clean, well-formatted document using the Quarto format. 
            Ensure you are adhering to the official Quarto file standard. 
            A Quarto file should start only with the Quarto metadata at the top of the file, 
            including the title, format, and any other relevant parameters.
            
            The following is a reference Quarto file you should use as a basis: 
            {template}"""
            },
            {"role": "user", 
            "content": f"""Please convert the following content into a {template_type} (.qmd) file. 
            - Ensure you're adhering to the provided Quarto template structure and formatting guidelines.
            - Ensure you dont start and end the file with the typical three markdown 
            backquotes (```) as it is not needed for Quarto.
            - Here is a presentation outline for you to use as a basis for the slides: 
            {outline}"""}
        ])

        try:
            client = OpenAI(api_key=api_key)        
            response = client.chat.completions.create(
                model= input.model(),
                messages=llm_prompt()
            )

            quarto_content.set(response.choices[0].message.content)
        except Exception as e:
            ui.notification_show(f"Error: {str(e)}", type="error")
    
    @output
    @render.text
    def quarto_output():
        if quarto_content():
            lines = quarto_content().split("\n")
            if lines[0].startswith("```") and lines[-1].startswith("```"):
                lines = lines[1:-1]
                return "\n".join(lines)
            else:
                return quarto_content()

    @output
    @render.download(
        filename=lambda: f"webpage_content{hash(input.outline())}.qmd",
    )
    async def download():
        await asyncio.sleep(0.25)
        yield quarto_content()

app = App(app_ui, server)
