from niwrap import fsl
from styxdefs import set_global_runner
from styxdocker import DockerRunner
from styxgraph import GraphRunner
import os

def anatomical_preprocessing(input_file):
    # Step 1: Reorient to standard space
    reorient_output = fsl.fslreorient2std(
        input_image=input_file,
    )

    # Step 2: Robustly crop the image
    robustfov_output = fsl.robustfov(
        input_file=reorient_output.output_image,
    )

    # Step 3: Brain extraction
    bet_output = fsl.bet(
        infile=robustfov_output.output_roi_volume,
        fractional_intensity=0.5,  # Fractional intensity threshold
        robust_iters=True,
        binary_mask=True,
        approx_skull=True,
    )

    # Step 4: Tissue segmentation
    seg_output = fsl.fast(
        in_files=[bet_output.outfile],
        img_type=3  # 3 tissue classes
    )

    print("Anatomical preprocessing completed.")
    return bet_output, seg_output

if __name__ == "__main__":
    input_file = r"C:\Users\floru\Downloads\T1.nii.gz"#"path/to/your/input/T1w.nii.gz"
    output_dir = "my_output"

    # Set up the Docker runner
    runner = DockerRunner(data_dir=output_dir)
    graph_runner = GraphRunner(base=runner)
    set_global_runner(graph_runner)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Run the anatomical preprocessing
    brain, segmentation = anatomical_preprocessing(input_file)

    print(graph_runner.node_graph_mermaid())