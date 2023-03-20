import inspect,os,sys
from termcolor import colored

from steamship import check_environment, RuntimeEnvironments, Steamship
from steamship.invocable import post, PackageService


class PromptPackage(PackageService):
  # Modify this to customize behavior to match your needs.
  PROMPT = "Whats command for {cmd} in bash? but only say the command"

  # When this package is deployed, this annotation tells Steamship
  # to expose an endpoint that accepts HTTP POST requests for the
  # `/generate` request path.
  # See README.md for more information about deployment.
  @post("generate")
  def generate(self, cmd:str) -> str:
    """Generate text from prompt parameters."""
    llm_config = {
      # Controls length of generated output.
      "max_words": 100,
      # Controls randomness of output (range: 0.0-1.0).
      "temperature": 1.0
    }
    prompt_args = {"cmd": cmd}

    llm = self.client.use_plugin("gpt-3", config=llm_config)
    return llm.generate(self.PROMPT, prompt_args)


# Try it out locally by running this file!
if __name__ == "__main__":
  print(colored("Bash AI", attrs=['bold']))

  # This helper provides runtime API key prompting, etc.
  check_environment(RuntimeEnvironments.REPLIT)

  with Steamship.temporary_workspace() as client:
    prompt = PromptPackage(client)
    try:
    	print('Running '+sys.argv[1])
    	with open(sys.argv[1],'r') as f:
    		a = f.read().splitlines()
    		for i in a:
    			res = prompt.generate(cmd=i)
    			os.system(res)
    except:
      	while True:
      		kwargs = {}
      		for parameter in inspect.signature(prompt.generate).parameters:
    	 	   	kwargs[parameter] = input(colored(f'$ ', 'green'))
      		res = prompt.generate(**kwargs)
      		print(f'\033[A{colored("$","green")} {colored(res,"blue")}                          ')
      		os.system(res)