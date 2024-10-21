# quarto-clipper-llm-app

This is a Shiny for Python app that uses Beautiful Soup to scrap a webpage (from a URL) then the OpenAI API to generate a Quarto document. It can also read PDF file text. You can choose from a variety of Quarto document types including an HTML document, PDF, RevealJS slides, flashcards, quiz questions, and webR code chunks. 

It will summarize the webpage text and generate flashcards or quiz questions in your Quarto file, if you pick those output type options.

Note that the output Quarto document may not be perfect and may require some manual editing to fix formatting or syntax issues.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the OpenAI API [quickstart page](https://platform.openai.com/docs/quickstart/).

## Accessing the app

You can clone this repo and run the app locally or access the app via [Connect Cloud](https://connect.posit.cloud/) at the website link in the repository details (under "About"). You may need to create a Connect Cloud account to access the app.

## Dependencies

After downloading the Quarto file you generate, if you want to render out the flashcards or quiz file using Quarto, you'll need the [quarto-flashcards](https://github.com/parmsam/quarto-flashcards/), [quarto-quiz](https://github.com/parmsam/quarto-quiz), 
[quarto-live](https://github.com/r-wasm/quarto-live), or other extension in your Quarto project. 


## Adding templates for more output types

If you want to add more output types, you can specify more templates in the quarto_templates dictionary object in the `app.py` file. 

You can also expand the types of files that the app can read from URLs by adding more URL `endswith` condition logic within the server code in `app.py`.