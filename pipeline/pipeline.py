import kfp
from kfp import dsl
from kfp import components as comp

create_step_collect_files = comp.load_component_from_text("""
name: Collect Files
description: Downloads files from Github Repository directory.

inputs:
- {name: user, type: String, default: 'DanielSCrouch', description: 'Github username.'}
- {name: repo, type: String, default: 'safe-intel', description: 'Github repository name.'}
- {name: branch, type: String, default: 'main', description: 'Github branch name.'}
- {name: subdirectory, type: String, default: 'files', description: 'Github sub-directory name.'}
- {name: outdir, type: String, default: '/mnt/files', description: 'Path to local directory to save files to.'}
outputs:
- {name: respath, type: Data, description: 'Path to file to save results to. Results are paths to each downloaded file.'}

implementation:
  container:
    image: index.docker.io/duartcs/filecollect:latest
    # command is a list of strings (command-line arguments). 
    # The YAML language has two syntaxes for lists and you can use either of them. 
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
      python3, 
      # Path of the program inside the container
      ./file-collect.py,
      --user,
      {inputValue: user},
      --repo,
      {inputValue: repo},
      --branch,
      {inputValue: branch},
      --subdirectory,
      {inputValue: subdirectory},
      --outdir,
      {inputValue: outdir},
      --respath,
      {outputPath: respath},
    ]""")


@dsl.pipeline(name='safe-intelligence-pipeline')
def pipeline():

    vop = dsl.VolumeOp(
    name="volume_creation",
    resource_name="mypvc",
    modes=kfp.dsl.VOLUME_MODE_RWO,
    size="1Gi"
    )

    collect_files_step = create_step_collect_files()

    collect_files_step.add_pvolumes({"/mnt'": vop.volume})

    print(collect_files_step.outputs)

    # with dsl.ParallelFor(collect_files_step.output) as item:
    #     op1 = dsl.ContainerOp(
    #         name="my-item-print",
    #         image="library/bash:4.4.23",
    #         command=["sh", "-c"],
    #         arguments=["echo do output op1 item: %s" % item],
    #     )

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.yaml')