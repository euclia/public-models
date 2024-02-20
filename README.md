# public-models
This repository contains the code that is relevant to the training of the Jaqpot public models. These are 22 ML/AI models,
trained on the data of the Therapeutics Data Commons ADME-Tox (ADMET) Benchmark group and are suitable for small molecule drug discovery.
The training datasets can be found at [Therepeutic Data Commons](https://tdcommons.ai/overview/).

These models are currently buildable using the scripts in the `src` directory (NOTE: the scripts must be run from within that directory):

| Prediction                | Training data                                                                                                                | Model Type       | Descriptors |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------|------------------|-------------|
| AMES                      | [4 papers](https://tdcommons.ai/single_pred_tasks/tox/#ames-mutagenicity)                                                    | SVC (C)          | Topo        |
| BBB                       | [Martins et al.](https://tdcommons.ai/single_pred_tasks/adme/#bbb-blood-brain-barrier-martins-et-al)                         | KNN (C)          | Mordred     |
| Bioavailability           | [Ma et al.](https://tdcommons.ai/single_pred_tasks/adme/#bioavailability-ma-et-al)                                           | KNN (C)          | MACCS       |
| Caco2                     | [Wang et al.](https://tdcommons.ai/single_pred_tasks/adme/#caco-2-cell-effective-permeability-wang-et-al)                    | RF (R)           | Mordred     |
| Hepatocyte Clearance      | [AZ](https://tdcommons.ai/single_pred_tasks/adme/#clearance-astrazeneca)                                                     | SVR (R)          | MACCS       |
| Microsomal clearance      | [AZ](https://tdcommons.ai/single_pred_tasks/adme/#clearance-astrazeneca)                                                     | SVR (R)          | Topo        |
| CYP2C9                    | [Carbon-Mangels et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp2c9-substrate-carbon-mangels-et-al)                  | BernoulliNB (C)  | MACCS       |
| CYP2C9                    | [Veith et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp-p450-2c9-inhibition-veith-et-al)                             | BernoulliNB (C)  | Topo        |
| CYP2D6                    | [Carbon-Mangels et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp2d6-substrate-carbon-mangels-et-al)                  | ComplementNB (C) | Topo        | 
| CYP2D6                    | [Veith et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp-p450-2d6-inhibition-veith-et-al)                             | BernoulliNB (C)  | Topo        |
| CYP3A4                    | [Carbon-Mangels et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp3a4-substrate-carbon-mangels-et-al)                  | ExtraTrees (C)   | RDKit       |
| CYP3A4                    | [Veith et al.](https://tdcommons.ai/single_pred_tasks/adme/#cyp-p450-3a4-inhibition-veith-et-al)                             | SVC (C)          | Topo        | 
| DILI                      | [US FDA](https://tdcommons.ai/single_pred_tasks/tox/#dili-drug-induced-liver-injury)                                         | RF (C)           | Mordred     |
| Half life                 | [Obach et al.](https://tdcommons.ai/single_pred_tasks/adme/#half-life-obach-et-al)                                           | SVR (R)          | Topo        |
| hERG                      | [648 drugs](https://tdcommons.ai/single_pred_tasks/tox/#herg-blockers)                                                       | SVC (C)          | MACCS       |
| HIA                       | [Hou et al.](https://tdcommons.ai/single_pred_tasks/adme/#hia-human-intestinal-absorption-hou-et-al)                         | LR (C)           | MACCS       |
| Accute toxicity LD50      | [Zhu et al.](https://tdcommons.ai/single_pred_tasks/tox/#acute-toxicity-ld50)                                                | RF (R)           | MACCS       |
| Lipophilicity             | [AZ](https://tdcommons.ai/single_pred_tasks/adme/#lipophilicity-astrazeneca)                                                 | SVR (R)          | Topo        |
| P-glycoprotein Inhibition | [Broccatelli et al.](https://tdcommons.ai/single_pred_tasks/adme/#pgp-p-glycoprotein-inhibition-broccatelli-et-al)           | RF (C)           | MACCS       |
| Plasma Protein Binding    | [AZ](https://tdcommons.ai/single_pred_tasks/adme/#ppbr-plasma-protein-binding-rate-astrazeneca)                              | RF (R)           | MACCS       |
| Solubility                | [9982 drugs](https://tdcommons.ai/single_pred_tasks/adme/#solubility-aqsoldb)                                                | SVR (R)          | MACCS       |
| VDss                      | [Lombardo et al.](https://tdcommons.ai/single_pred_tasks/adme/#vdss-volumn-of-distribution-at-steady-state-lombardo-et-al)   | SVR (R)          | Topo        |

Codes:
* BBB - Blood-Brain Barrier
* DILI - Drug Induced Liver Injury
* KNN - K-nearest neighbours
* LR - Logistic Regression
* HIA - Human Intestinal Absorption
* MACCS - MACCS keys
* Mordred - Mordred descriptors
* RF - Random Forest
* Topo - topological fingerprints
* VDss - Volume of Distribution at steady state
* Codes for model type (C)=classification, (R)=Regression 

# Setup

Create a virtualenv in which to run the code.

```commandline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# To run

To build the models you need to be in the src directory and then run like this:

python3 filename.py -r <run_as>

The run_as must be one of the following and cannot be omitted:
 - single (to train the model a single time)
 - cross (for cross validation of the model)
 - deploy (to cross validate the model and upload it on Jaqpot)
 - save (save the model to a local file)
