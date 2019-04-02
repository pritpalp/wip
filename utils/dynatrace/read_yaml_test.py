import yaml
import io

filename = "dynatrace_conf.yaml"
# open the file
with open(filename, 'r') as f:
  try:
    docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in docs:
      for k,v in doc.items():
        if "name" in k:
          print k, "->", v
        if "url" in k:
          print k, "->", v
      print "\n"
  except yaml.YAMLError as exc:
    print(exc)
