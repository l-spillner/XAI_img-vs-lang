# Explanation Modality in Explainable AI: visual vs. natural language explanations

### Dataset

- subset of student corpus
- under data there is dataset_students (which is the OG dataset) and data_set values, which maps the feature value keys to their actual descriptive names, as well as the names of the features to the more easily understandable ones we came up with. I used this by reading it line by line and converting it into a dict like this:
- the model trained for the task (LightGBM, so basically a forest) is included under data as well. I only included a smaller part of the dataset and reduced some parameters to have the model be not too good (the trust task is useless if it's always smartest to just go with the AI no matter what it says).
- shap was used to generate local feature importance explanations, which can be seen in the Generate_vis_explanations notebook
- I did this for all of the students in the test dataset, and then among them selected a subset of students in the following way:
    - identified the most important, second most important, and third most important feature for all students
    - grouped them by which feature was top 1, top 2, top 3
    - chose one student randomly* of each group, so for all the features that were top 1 at least once one student were this was the case, and then again for all top 2 features and so on
    - * but not with even distribution, but rather based on strong that feature was, so that I was more likely to get a case were this feature was more important
    - this way, since I also did it for top 2 and top 3, features that are very often the top 1 or top 2 feature should appear more often among those, so that there is exactly one case for each top one but at least one, with those that are more common appearing more often
 - for this subset, the data of the explanation (feature importance for all features with impact above 1%) is saved in explanations.json
 
### Explanations

- for all of them, visual explanations were generated (see folder explanations_vis)
    - x-axis is -0.5 to 0.5, so the middle is no impact, to the left is negative impact and to the right positive impact
    - the base chance is about 60% probability to graduate, so the bar for basechance is at about +10% (because it is a positive impact compared to 50/50 chance)
    - "other" includes everything under 1%
    - the reason why the pics are so much bigger than their content is because it was the only way I could get matplotlib to generate images were the bars are always the same size and the scale does not change. For the only study, we might have to crop these manually?
- for all of them, natural language explanations were generated with GPT-4 (explanations_lang.json)
    - this file also contains the explanation data used to generate them, so you only need to read this file
    - I prompted GPT-4 with an example from my tests which I thought was good, because otherwise the results differed wildly
    - it does not always include all of the data even though I really tried hard to tell it to do so - this is probably not avoidable
    - it does sometimes make mistakes like saying something that had positive impact is negative or vice versa, but it's way better at it than GPT-3.5

### Examples

- to look at some examples, open the generate_lang_explanations notebook, at the bottom I printed some examples of the texts together with the respective students images
