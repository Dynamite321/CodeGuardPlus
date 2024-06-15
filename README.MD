# Constrained Decoding for Secure Code Generation
We propose a test suite CodeGuard+ to evaluate both security and correctness of Code LLMs. We also propose to use constrained decoding techniques to make Code LLMs to generate secure and correct code. More details can be found in the [paper](https://arxiv.org/abs/2405.00218).

## Directory Structure
The directory structure of this repository is as follows:
```
.
|-- prompts                    # All prompts.
    |-- CWE
        |-- prompt
|-- unit_tests                 # Unit tests for each prompt
    |-- CWE
        |-- prompt
            |-- functional.py  # Individual unit test
|-- requirements.txt           # Python packages needed by prompts and unit tests
```

## Test suite
Our test suite CodeGuard+ is adapted from [Copilot Dataset](https://arxiv.org/abs/2108.09293) and [SecurityEval](https://dl.acm.org/doi/abs/10.1145/3549035.3561184). It now includes 91 prompts covering 34 CWEs, along with corresponding unit tests and CodeQL queries. You can find prompts and CodeQL queries in `prompts` and unit_tests in `unit_tests`.

## Run unit tests
Here is an example of how to run unit tests. To run the unit test for the completed programs of prompt CWE-020 1-py, the following commands are needed:
```sh
cd unit_tests/cwe-020/1-py
python functional.py --path {the_path_to_completions}
```

## Work in Progress
This repository is still under construction, thank you for your patience! 

## Citation
```
@article{fu2024constrained,
      title={Constrained Decoding for Secure Code Generation}, 
      author={Yanjun Fu and Ethan Baker and Yu Ding and Yizheng Chen},
      year={2024},
      journal={arXiv preprint arXiv:2405.00218}
}
```