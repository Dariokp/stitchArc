#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=18
#SBATCH --gpus=1
#SBATCH --partition=gpu_a100
#SBATCH --time=12:00:00
#SBATCH --job-name=Stitch
#SBATCH --output=slurm_output_%A.out

# Loading modules (CUDA and Anaconda are located in module 2024)
module load 2024
module load CUDA/12.6.0
module load Anaconda3/2024.06-1

# Logging info
echo "Starting job at $(date)"

# Change working directory
cd "$TMPDIR" # $TMPDIR is set to /scratch-local/username

# Copy transduction data to local scratch
if cp -r $HOME/stitchArc/src/stitchArc/stitch_functions "$TMPDIR"; then
    echo "data copied to scratch: $HOME/stitchArc/src/stitchArc/stitch_functions --> $TMPDIR/stitch_functions"
else
    echo "Error: Failed to copy data from $HOME/stitchArc/src/stitchArc/stitch_functions to $TMPDIR"
    exit 1
fi

# Activate conda environment
source activate arcProjectEnv

# Run the python script
srun python $HOME/stitchArc/src/stitchArc/run_stitch.py

# Copy output directory from scratch back to desired directory
cp stitch_output.json $HOME/stitchArc/src/stitchArc

echo "Finished job at $(date)"