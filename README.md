### Sagemaker folder

model.py : Used to locally train a Sklearn model. Uses joblib module to save the trained model.<br>
model.joblib : Saves the locally trained model in the format that SageMaker is expecting for Sklearn models<br>

inference.py : Helps SageMaker understand how input and output for the model will be configured<br>

main.py : Script to deploy model onto SageMaker<br>
invoke.py : Script that tests the endpoint by invoking it<br>

___________________________________________________________________________________________________

### Website folder

index.html : Homepage of music recommendation web app<br>
styles.css : Styling for the index file<br>

script.js : Handles all logic of frontend (calling Spotify API and my API)<br>

___________________________________________________________________________________________________

### Lambda folder

lambda_function.py : Code deployed on AWS Lambda to call SageMaker endpoint
