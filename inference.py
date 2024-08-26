"""
The following is a simple example algorithm.

It is meant to run within a container.

To run it locally, you can call the following bash script:

  ./test_run.sh

This will start the inference and reads from ./test/input and outputs to ./test/output

To export the container and prep it for upload to Grand-Challenge.org you can call:

  docker save example-algorithm-preliminary-docker-evaluation | gzip -c > example-algorithm-preliminary-docker-evaluation.tar.gz

Any container that shows the same behavior will do, this is purely an example of how one COULD do it.

Happy programming!
"""

from glob import glob
from pathlib import Path
import SimpleITK
import json

def run():
    INPUT_PATH = Path("/input")
    OUTPUT_PATH = Path("/output")
    RESOURCE_PATH = Path("resources")

    # Read input data.
    ''' TODO- uncomment the image modalities you use in your algorithm.
        In this example, we only use preprocessed_tmax.'''

    # 1) Reading 'raw_data' inputs.
    # 1.1) CT images.

    # non_contrast_ct = load_image_file_as_array(
    #     location=INPUT_PATH / "images/non-contrast-ct",
    # )
    # ct_angiography = load_image_file_as_array(
    #     location=INPUT_PATH / "images/ct-angiography",
    # )
    # perfusion_ct = load_image_file_as_array(
    #     location=INPUT_PATH / "images/perfusion-ct",
    # )
    #
    # # 1.2) Perfusion maps.
    # tmax_parameter_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/tmax-parameter-map",
    # )
    # cbf_parameter_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/cbf-parameter-map",
    # )
    # cbv_parameter_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/cbv-parameter-map",
    # )
    # mtt_parameter_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/mtt-parameter-map",
    # )


    # # 2) Reading 'derivatives' inputs.
    # # 2.1) CT images.
    #
    # preprocessed_ct_angiography = load_image_file_as_array(
    #     location=INPUT_PATH / "images/preprocessed-CT-angiography",
    # )
    # preprocessed_perfusion_ct = load_image_file_as_array(
    #     location=INPUT_PATH / "images/preprocessed-perfusion-ct",
    # )
    #
    # # 2.2) Perfusion maps.
    preprocessed_tmax_map = load_image_file_as_array(
        location=INPUT_PATH / "images/preprocessed-tmax-map",
    )
    # preprocessed_cbf_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/preprocessed-cbf-map",
    # )
    # preprocessed_cbv_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/preprocessed-cbv-map",
    # )
    #
    # preprocessed_mtt_map = load_image_file_as_array(
    #     location=INPUT_PATH / "images/preprocessed-mtt-map",
    # )

    # 3) Reading 'phenotype' (clinical 'baseline' tabular data)
    #acute_stroke_clinical_information = json.load(open(INPUT_PATH / "acute-stroke-clinical-information.json"))


    # using resources.
    # with open(RESOURCE_PATH / "some_resource.txt", "r") as f:
    #     print(f.read())
    # Prediction scripts come below.
    ################################################################################################################
    #################################### here comes your predictions algorithm  ####################################
    #_show_torch_cuda_info() # comment out to test pytorch/cuda
    stroke_lesion_segmentation = predict_infarct(preprocessed_tmax_map) # todo -function to be updated by you!
    ################################################################################################################

    # Save your output
    write_array_as_image_file(
        location=OUTPUT_PATH / "images/stroke-lesion-segmentation",
        array=stroke_lesion_segmentation,
    )

    return 0


def load_image_file_as_array(*, location):
    # Use SimpleITK to read a file
    input_files = glob(str(location / "*.mha"))
    result = SimpleITK.ReadImage(input_files[0])

    # Convert it to a Numpy array
    return SimpleITK.GetArrayFromImage(result)


def write_array_as_image_file(*, location, array):
    location.mkdir(parents=True, exist_ok=True)

    suffix = ".mha"
    print(str(location / f"output{suffix}"))
    image = SimpleITK.GetImageFromArray(array)
    print(sum(image))
    SimpleITK.WriteImage(
        image,
        location / f"output{suffix}",
        useCompression=True,
    )


def predict_infarct(preprocessed_tmax, cutoff=9):
    ''' We are creating a simple lesion prediction based on the introductory Git-Repository example:
    https://github.com/ezequieldlrosa/isles24
    In this exapmle, we load the preprocessed Tmax map and threshold it at a cutoff of 9 (s).'''

    ################################################################################################################
    #################################### Beginning of your prediction method. ######################################
    # todo replace with your best model here!

    prediction = preprocessed_tmax > cutoff
    ################################################################################################################

    return prediction.astype(int)


def _show_torch_cuda_info():
    import torch

    print("=+=" * 10)
    print("Collecting Torch CUDA information")
    print(f"Torch CUDA is available: {(available := torch.cuda.is_available())}")
    if available:
        print(f"\tnumber of devices: {torch.cuda.device_count()}")
        print(f"\tcurrent device: { (current_device := torch.cuda.current_device())}")
        print(f"\tproperties: {torch.cuda.get_device_properties(current_device)}")
    print("=+=" * 10)
if __name__ == "__main__":
    raise SystemExit(run())
