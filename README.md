# ukrmolmatreader
Python package to read K-matrix files produced by the UKRmol software as found here:
https://ccpforge.cse.rl.ac.uk/gf/project/ukrmol-out/.

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/ukrmolmatreader.git
    cd ukrmolmatreader
    python setup.py install
    
## Dependencies
Author packages (these will have their own dependencies):
 - [pynumwrap](https://github.com/petersbingham/pynumwrap)
 - [tisutil](https://github.com/petersbingham/tisutil) (optional)
 - [channelutil](https://github.com/petersbingham/channelutil) (optional)
    
## Usage

Call the `read_Kmats(file_path, asymcalc=None, source_str=None)` with the path to your UKRmol K-matrix file. Note that the energies from the start to the end of the file must be in ascending order.
There are two returned values:
  1.  A dictionary keyed by energy with matrices as values. Or a `tisutil.dKmat` if the `tisutil` module is available; the `dKmat` will require a `channelutil.AsymCalc` like object and a `source_str`, which can be passed as the optional parameters to `read_Kmats` (see [channelutil](https://github.com/petersbingham/channelutil) and [tisutil](https://github.com/petersbingham/tisutil) for further details). 
  2.  A list describing different open channels across the energy range. Each element in the list is another list describing that open channel; the first element is the number of open channels and the second is a two element list giving the starting and one past the end index of the range overwhich the set of open channels apply. This index will apply to a sorted list of the dictionary energies. This is clarified in the example below.

There are two types that the ukrmolmatreader is compatible with, standard python types and mpmath types. Python types is the default. To change to mpmath types call the module function `use_mpmath_types()`.

The following example illustrates. Explanation follows.
```python
>>> import ukrmolmatreader as matread
>>> module_dir = os.path.dirname(os.path.realpath(matread.__file__))
>>> kmats,o_chan_desc = matread.read_Kmats(module_dir+"/tests/water_inel_B1_10ch.19")
>>> o_chan_desc
[[4, [0, 1025]], [10, [1025, 1800]]]
>>> first = o_chan_desc[0][1][0]
>>> firstEne = sorted(kmats.keys())[first]
>>> kmats[firstEne]
matrix([[-0.44319103+0.j,  0.17810525+0.j,  0.00342772+0.j, -0.03147134+0.j],
        [ 0.17810525+0.j, -0.00818044+0.j,  0.09482788+0.j, -0.00245007+0.j],
        [ 0.00342772+0.j,  0.09482788+0.j, -0.03620601+0.j,  0.01289757+0.j],
        [-0.03147134+0.j, -0.00245007+0.j,  0.01289757+0.j, -0.00201263+0.j]])
```
The o_chan_desc `[[4, [0, 1025]], [10, [1025, 1800]]]` means the following:
 * `[4, [0, 1025]]` refers to the channels below the first threshold. There are four channels, extending from the zero index to 1024 (one past the end used).
 * `[10, [1025, 1800]]` refers to the channels between the first and second thresholds. There are ten channels, extending from the 1025 index to 1799 (one past the end used).
 * Again, it is important to note that the indices apply to the sorted range of dictionary keys ie. to the list returned from `kmats.keys()`.
