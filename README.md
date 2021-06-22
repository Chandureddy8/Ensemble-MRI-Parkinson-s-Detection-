# Ensemble-MRI-Parkinson-s-Detection-
Early detection method for parkinson's disease using deep ensemble learning on MRI dataset
Parkinson's disease (PD) belongs to a group of conditions called motor system disorders, which cause unintended or uncontrollable movements of the body.  The precise cause of PD is unknown, but some cases are hereditary while others are thought to occur from a combination of genetics and environmental factors that trigger the disease.  In PD, brain cells become damaged or die in the part of the brain that produces dopamine--a chemical needed to produce smooth, purposeful movement.

The four primary symptoms of PD are:

tremor--shaking that has a characteristic rhythmic back and forth motion
rigidity--muscle stiffness or a resistance to movement, where muscles remain constantly tense and contracted
bradykinesia--slowing of spontaneous and automatic movement that can make it difficult to perform simple tasks or rapidly perform routine movements
postural instability--impaired balance and changes in posture that can increase the risk of falls.
Other symptoms may include difficulty swallowing, chewing, or speaking; emotional changes; urinary problems or constipation; dementia or other cognitive problems; fatigue; and problems sleeping.

PD usually affects people around the age of 70 years but can occur earlier.  Women are more affected by PD.  Currently there are no specific tests that diagnose sporadic PD.

For the detection of pd, i have used MRI images from PPMI website (https://www.ppmi-info.org/access-data-specimens/download-data/)
Images are in t2 weigthed,Axial plane.........


# How to Improve Performance By Combining Predictions From Multiple Models
![alt text](https://github.com/Chandureddy8/Ensemble-MRI-Parkinson-s-Detection-/blob/main/test%20images/1_1ArQEf8OFkxVOckdWi7mSA.png)

A successful approach to reducing the variance of neural network models is to train multiple models instead of a single model and to combine the predictions from these models. This is called ensemble learning and not only reduces the variance of predictions but also can result in predictions that are better than any single model.

Ensemble learning combines the predictions from multiple neural network models to reduce the variance of predictions and reduce generalization error.

Model averaging is an ensemble technique where multiple sub-models contribute equally to a combined prediction.

Model averaging can be improved by weighting the contributions of each sub-model to the combined prediction by the expected performance of the submodel. This can be extended further by training an entirely new model to learn how to best combine the contributions from each submodel. This approach is called stacked generalization, or stacking for short, and can result in better predictive performance than any single contributing model.

There are several ways to perform ensemble learning, and a reasonable summary is available on (https://en.wikipedia.org/wiki/Ensemble_learning) Simply speaking, there are two major classes of ensemble learning:

Bagging: fit independent models and then average their predictions
Boosting: fit several models sequencially and then average their predictions
