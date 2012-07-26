git submodule init
git submodule update

cd lib/ply            && python setup.py build && cd ../../ && ln -s lib/ply/build/lib/ply
