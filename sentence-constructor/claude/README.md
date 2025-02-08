# Claude AI Prompt Engineering Guide

## Model
Claude Sonnet 3.5 

## prompting guid
[documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)


### Create an initial prompt
Refer to [prompt iterations](./prompt_iterations.md)
### Explore using xml tag
Using the final prompt from the propt iterations, I tried restructure it with xml tag to be more concise
Refer to [prompt iteration xml](./prompt_iterations_xml.md)

#### Using dashboard function
while reading and exploring claude workbench, I noticed that it is possible to build prompt using their dashboard tools.
[Dashboard](https://console.anthropic.com/dashboard)

```
To crate a japanese language teacher that focus on short sentences, on recognising and writing with JPLT level 5 vocabulary, it should focus on recall  and feedback. The progress should be trackable. Please do not give answer but rather give hints on how far or close and constructive feedback that can be improve upon. The communication should be in Japanese and English but progressively move towards fully japanese.
```

### Iteration flow
1. [basic_prompting.md](./iterations/basic_prompting.md)
2. proceed with the prompt by testing it in the workbench.
3. testing the prompt in the workbench 
   1. Examples -> click on add examples, generate variable values
      - check if the variable values generated actually simulate the typical exchange expected between student and teacher.
      - check the generation logic which allows you to update the logic. [Generation Logic](./generation_logic.md)
4. provide improvement using improve prompt [Improvement](./iterations/improvement_v2.md)
5. Back to step 1. 

## Thoughts

1. There's quite a comprehensive support for prompt engineering.
2. Their tools help to understand how to improve. e.g (improve prompts, examples, evaluate, generate examples)
3. By using generate examples, I noticed that I need to be specific about student are english speaking while the teacher should be Native japanese speaker.

## Conclusion
I think using xml tag for prompting for this use case is the most effective and more intuitive.