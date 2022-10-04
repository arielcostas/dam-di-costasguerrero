import os

for file in os.listdir(os.getcwd()):
	if file.endswith("ui"):
		filename = file.split(".")[0]
		command = f"{os.getenv('LOCALAPPDATA')}\\Programs\\Python\\Python310\\Scripts\\pyuic6.exe {filename}.ui -o {filename}.py"
		os.system(command)
		print(f"Recompilado {filename}.ui a {filename}.py")