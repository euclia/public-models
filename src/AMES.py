from jaqpotpy.models.evaluator import Evaluator
from jaqpotpy.models import MolecularSKLearn
from jaqpotpy.datasets import SmilesDataset
from jaqpotpy.descriptors.molecular import TopologicalFingerprint
from jaqpotpy import Jaqpot
from jaqpotpy.doa.doa import Leverage
from tdc.benchmark_group import admet_group
from src.helpers import get_dataset, cross_train_sklearn
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.svm import SVC

import argparse
import json


# Argument to control the execution of the code
argParser = argparse.ArgumentParser()
argParser.add_argument("-r", "--run-as", help="""'single' to train the model a single time or \n
                                              'cross' for cross validation of the model or \n
                                              'deploy' to cross validate the model and upload it on Jaqpot""")
args = argParser.parse_args()


# Get the data using the TDC client
group = admet_group(path = 'data/')
benchmark, name = get_dataset('AMES', group)

train_val = benchmark['train_val']
test = benchmark['test']

# Declare the model's algorithm
svm = SVC(C=40, kernel='rbf',gamma=0.05, random_state=42)


# Declare the Featurizer and the Evaluator's metrics
featurizer = TopologicalFingerprint()

val = Evaluator()
val.register_scoring_function('ACC', accuracy_score)
val.register_scoring_function('AUC', roc_auc_score)


# Train model once in order to find the best algorithm and optimize it
if args.run_as == 'single':

    # Train - Validation split
    train, valid = group.get_train_valid_split(benchmark = name, split_type = 'default', seed = 42)

    # Create the Jaqpot Datasets
    jaq_train = SmilesDataset(smiles = train['Drug'], y = train['Y'], featurizer = featurizer, task='classification')
    jaq_train.create()

    jaq_val = SmilesDataset(smiles = valid['Drug'], y = valid['Y'], featurizer = featurizer, task='classification')
    jaq_val.create()

    # Update the Evaluator's dataset
    val.dataset = jaq_val

    # Train the model
    model = MolecularSKLearn(jaq_train, doa=Leverage(), model=svm, eval=val)
    _ = model.fit()


elif args.run_as in ['cross', 'deploy']:

    # Create a dummy Jaqpot model class
    dummy_train = SmilesDataset(smiles=train_val['Drug'], y=train_val['Y'], featurizer=featurizer)
    model = MolecularSKLearn(dummy_train, doa=Leverage(), model=svm, eval=val)

    # Cross Validate and check robustness
    evaluation = cross_train_sklearn(group, model, name, test, 'classification')
    print('\n\nEvaluation of the model:', evaluation)

    # Upload on Jaqpot
    if args.run_as == 'deploy':

        # Merge train and validation datasets
        train = SmilesDataset(smiles = train_val['Drug'], y = train_val['Y'], featurizer = featurizer, task='classification')
        train.create()

        test = SmilesDataset(smiles = test['Drug'], y = test['Y'], featurizer = featurizer, task='classification')
        test.create()

        # Update Evaluator's dataset
        val.dataset = test

        # Train the final model
        model = MolecularSKLearn(train, doa=Leverage(), model=svm, eval=val)
        final_model = model.fit()

        # Jaqpot Login
        jaqpot = Jaqpot()
        jaqpot.request_key_safe()

        # Deploy model
        final_model.deploy_on_jaqpot(jaqpot=jaqpot,
                                     description="Tox model the result of an AMES experiment. The Ames test is a short-term bacterial reverse mutation assay detecting a large number of compounds which can induce genetic damage and frameshift mutations.",
                                     model_title="AMES Model")

        # Opening Submission JSON file
        with open('data/submission_results.json', 'r') as openfile:
            # Reading from json file
            submission = json.load(openfile)

        submission[name] = evaluation[name]
        with open("data/submission_results.json", "w") as outfile:
            json.dump(submission, outfile)

else:
    raise ValueError(f'Argument {args.run_as} is not acceptable. Users must provide either "single" or "cross" or "deploy"')