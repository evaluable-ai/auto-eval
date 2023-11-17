# Evaluable AI

Welcome to Evaluable AI's open-source repository, featuring our flagship tool, AutoEval. AutoEval revolutionizes the way models are evaluated in production environments. It excels at thorough assessments, offering capabilities to compare outputs across different models or delve into the nuances of various responses within a single model. Its hallmark is a customizable scoring system, empowering users to define their evaluation criteria via a user-defined rubric.

**Key Features:**

- **Real-Time Output Generation:** Utilize AutoEval to generate and compare outputs from multiple models in real time, thanks to seamless API integration.
- **Comparative Analysis:** Effortlessly compare model outputs side-by-side, gaining deeper insights into their performance.
- **Customizable Scoring:** Tailor your evaluation criteria with our flexible scoring rubric, aligning it with your specific goals.
- **Ready-to-Use Templates:** Jumpstart your evaluation process with our range of pre-designed templates and examples, designed for user convenience.

## Getting Started

## API Key Setup

To use AutoEval effectively, you need to set up API keys for OpenAI and Hugging Face. Here's how you can do it:

### Setting up OpenAI API Key

 **Setting the Environment Variable:**
   - **For Windows Users:**
     - Open Command Prompt and type:
       ```cmd
       setx OPENAI_API_KEY "your_openai_api_key"
       ```
     - Replace `your_openai_api_key` with your actual API key from OpenAI.
     - Restart any open Command Prompt windows to apply the changes.

   - **For macOS/Linux Users:**
     - Open Terminal and edit your shell profile file (like `~/.bashrc`, `~/.zshrc`, etc.) by typing `nano ~/.bashrc` or an equivalent command.
     - Add the following line at the end of the file:
       ```bash
       export OPENAI_API_KEY="your_openai_api_key"
       ```
     - Replace `your_openai_api_key` with your actual API key from OpenAI.
     - Save the file and exit the editor. Then, type `source ~/.bashrc` to apply the changes.


### Installation

Ensure your Python version is 3.0 or higher. Install AutoEval using pip:

```bash
pip install evaluableai
```

## Running Evaluations

### Basic Evaluation

Here's how to perform a basic evaluation:

```python
from evaluableai.evaluableai import EvaluableAI

data = [{
    'input': 'Who is the founder of Google?',
    'context': "Google was founded by Larry Page and Sergey Brin...",
    'responses': ['Sergey Brin and Larry Page founded Google in...', 'Larry and Sergey created Google']
}]

evaluator = EvaluableAI()
evaluator.run_with_user_data(data)
```

### Evaluation with Custom OpenAI Model

To use a custom OpenAI model for response evaluation:

```python
from evaluableai.evaluableai import EvaluableAI
from evaluableai.models.evaluation_models.evaluating_model_name import EvaluatingModelName
from evaluableai.models.evaluation_models.evaluating_model import EvaluatingModel

# Your data setup...

data = [{
    'input': 'Who is the founder of Google?',
    'context': "Google was founded by Larry Page and Sergey Brin...",
    'responses': ['Sergey Brin and Larry Page founded Google in...', 'Larry and Sergey created Google']
}]

evaluating_model = EvaluatingModel(EvaluatingModelName.OPENAI, 'gpt-3.5-turbo', 'OPENAI_API_KEY')
evaluator = EvaluableAI(evaluating_model=evaluating_model)
evaluator.run_with_user_data(data)
```

### On-the-Fly Output Generation with Multiple Candidate Models

To generate outputs on the fly using different candidate models:

```python
from evaluableai.evaluableai import EvaluableAI
from evaluableai.models.evaluation_models.evaluating_model_name import EvaluatingModelName
from evaluableai.models.evaluation_models.evaluating_model import EvaluatingModel
from evaluableai.models.candidate_models.candidate_model_names import CandidateModelName 
from evaluableai.models.candidate_models.candidate_model import CandidateModel

data = [{
    'input': 'Who is the founder of Google?',
    'context': "Google was founded by Larry Page and Sergey Brin...",
    'responses': ['Sergey Brin and Larry Page founded Google in...', 'Larry and Sergey created Google']
}]

# Your data setup...

candidate_1 = CandidateModel(CandidateModelName.OPEN_AI, 'meta-llama/Llama-2-7b-chat-hf', 'HUGGING_FACE_API_KEY')
candidate_2 = CandidateModel(CandidateModelName.HUGGING_FACE, 'Mistral-7B-v0.1', 'HUGGING_FACE_API_KEY')
evaluating_model = EvaluatingModel(EvaluatingModelName.OPENAI, 'gpt-3.5-turbo', 'OPENAI_API_KEY')
    
evaluator = EvaluableAI(evaluating_model=evaluating_model, candidate_models_list=[candidate_1, candidate_2])
evaluator.run_with_user_data(data)
```
