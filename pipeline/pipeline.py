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

create_step_upload_files = comp.load_component_from_text("""
name: Upload File
description: Uploads a file to MinIO Bucket. 

inputs:
- {name: filepath, type: String, default: '/tmp/test-file-1.txt', description: 'Path to file for upload.'}
- {name: storageurl, type: String, default: '18.132.68.212:8082', description: 'URL of MinIO Cloud storage.'}
- {name: accesskey, type: String, default: 'admin', description: 'Access key for MinIO Cloud storage.'}
- {name: secretkey, type: String, default: 'admin1234', description: 'Secret key for MinIO Cloud storage.'}
- {name: region, type: String, default: 'test', description: 'MinIO Cloud storage region.'}
- {name: bucket, type: String, default: '', description: 'MinIO Cloud storage bucket.'}
outputs:
- {name: respath, type: Data, description: 'Path to file to save results to. Result is bucket/filename.'}

implementation:
  container:
    image: index.docker.io/duartcs/fileupload:latest
    # command is a list of strings (command-line arguments). 
    # The YAML language has two syntaxes for lists and you can use either of them. 
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
      python3, 
      # Path of the program inside the container
      ./file-upload.py,
      --filepath,
      {inputValue: filepath},
      --storageurl,
      {inputValue: storageurl},
      --accesskey,
      {inputValue: accesskey},
      --secretkey,
      {inputValue: secretkey},
      --region,
      {inputValue: region},
      --bucket,
      {inputValue: bucket},
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

    print(collect_files_step.output)

    with dsl.ParallelFor(collect_files_step.output) as item:
      upload_file_step = create_step_upload_files(filepath=item)
      upload_file_step.add_pvolumes({"/mnt'": vop.volume})

    print("finished...") 

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.yaml')