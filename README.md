# quarto-clipper-llm-app

This is a Shiny for Python app that uses the OpenAI API to generate RevealJS presentation based in a Quarto document. Enter the outline for your slides and your OpenAI API key to get started. This app is based on the [Quarto Clipper](https://github.com/parmsam/quarto-clipper-llm-app) app I made before.

It will summarize the webpage text and generate flashcards or quiz questions in your Quarto file, if you pick those output type options.

Note that the output Quarto document may not be perfect and may require some manual editing to fix formatting or syntax issues.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the OpenAI API [quickstart page](https://platform.openai.com/docs/quickstart/).

## Accessing the app

You can clone this repo and run the app locally or access the app via [Connect Cloud](https://connect.posit.cloud/) at the website link in the repository details (under "About"). You may need to create a Connect Cloud account to access the app.

## Dependencies

You will need [Quarto](https://quarto.org/) to render the document 
into a RevealJS presentation.

## Adding templates for more output types

If you want to add more output types, you can specify more templates in the quarto_templates dictionary object in the `app.py` file.