#!/bin/zsh

# Reset environment options
emulate -LR zsh

# Get absolut path of script
mypath=$(dirname ${0:A})

# Say hello
echo "*********************"
echo "Setup for lepg on OSX"
echo "*********************"

# Check if brew is installed
echo ""
echo "Check for Homebrew, which is needed to download all the other libs needed."

which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    echo ""
    echo "Homebrew is not installed."
    echo "Homebrew will be installed now."
    echo ""
    echo "Please follow the instructions."
    echo 'Press any key to continue...'; read -k1 -s

    # Execute Homebrew installation script
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"



else
    # Brew is installed, we just do an update
    echo ""
    echo "Homerew is already installed."
    echo "We just do an update now."
    echo 'Press any key to continue...'; read -k1 -s
    echo ""
    brew update
fi

# Now install gcc which contains Fortran
echo ""
echo "Now we install the package containing Fortran."
echo 'Press any key to continue...'; read -k1 -s

brew install gcc

# We are ready to compile now
echo ""
echo "All libs we need are installed now and up to date."
echo "We can now compile lepg..."
echo 'Press any key to continue...'; read -k1 -s
echo ""
echo "Compiling the pre-processor..."

sourcefile="pre-processor.f"
outfile="pre-processor-osx.o"
locpath="pre1.6"

gfortran -w -o ${mypath}/${locpath}/${outfile} ${mypath}/${locpath}/${sourcefile}

ls -al ${mypath}/${locpath}

echo ""
echo "In the file list above you should now see an executable named ${outfile}"

echo 'Press any key to continue...'; read -k1 -s
echo ""
echo "Compiling the processor..."

sourcefile="leparagliding.f"
outfile="processor-osx.o"
locpath="lep"

gfortran -w -o ${mypath}/${locpath}/${outfile} ${mypath}/${locpath}/${sourcefile}

ls -al ${mypath}/${locpath}

echo ""
echo "In the file list above you should now see an executable named ${outfile}"
echo 'Press any key to continue...'; read -k1 -s

echo ""
echo "All preparations are done."
echo "You are ready to use lepg"
