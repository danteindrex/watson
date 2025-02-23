from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://au-syd.ml.cloud.ibm.com",
    api_key = "p-2+Jb8BsGbXnzuXUqgZxOQeJQ==;JOL/e+FGv/Z8Tn9SvJ6c+g==:AXXm5Cfvbgmi7yzSExqgQDOnDs8wOLxJqIC1YzHqmzdWTj/RMuIDF23YW2KBiKbvdy/dPqwX8iqIy+a8iEXPa3Vq0AulBAxYsw==",
)

client = APIClient(credentials)

model = ModelInference(
  model_id="ibm/granite-3-8b-instruct",
  api_client=client,
  project_id="a11a0d60-cd98-41d1-88f0-1641bae2ed93",
  params = {
      "max_new_tokens": 100
  }
  
)

prompt = 'How far is Paris from Bangalore?'
print(model.generate(prompt))
print(model.generate_text(prompt))


