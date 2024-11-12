from pymatgen.core import Structure
from pymatgen.core.lattice import Lattice
from ase import Atoms
from ase.visualize import view

def create_tmd_structure(metal, chalcogen, size=(1, 1, 1), output_name='TMD_structure'):
    """
    Create a 1H TMD structure based on provided atomic positions and lattice parameters.
    """
    # Define lattice parameters for 1H TMD structure
    a = 3.32226019  # In-plane lattice constant in Angstroms
    c = 13.54295655  # Out-of-plane thickness for 1H TMD in Angstroms

    # Lattice vectors for hexagonal system
    lattice = Lattice.from_parameters(a, a, c, 90, 90, 120)

    # Define atomic positions for TMD based on selected metal and chalcogen
    species = [metal, metal, chalcogen, chalcogen, chalcogen, chalcogen]  # 2 metals and 4 chalcogens
    positions = [
        [2/3, 1/3, 0.75],  # Metal 0
        [1/3, 2/3, 0.25],  # Metal 1
        [1/3, 2/3, 0.87222232],  # Chalcogen 2
        [2/3, 1/3, 0.37222232],  # Chalcogen 3
        [1/3, 2/3, 0.62777768],  # Chalcogen 4
        [2/3, 1/3, 0.12777768]   # Chalcogen 5
    ]

    # Create the base structure
    base_structure = Structure(lattice, species, positions)

    # Scale the structure to the specified supercell size
    structure = base_structure * size

    # Save the structure in CIF format
    structure.to(fmt='cif', filename=f'{output_name}.cif')
    print(f"Structure saved as {output_name}.cif")

    # Convert pymatgen structure to ASE Atoms
    ase_structure = Atoms(
        symbols=[str(s) for s in structure.species],
        positions=structure.cart_coords,  # Use cart_coords from pymatgen
        cell=structure.lattice.matrix,
        pbc=True  # Periodic boundary conditions
    )

    # Visualize the structure using ASE
    view(ase_structure)

# User inputs
if __name__ == "__main__":
    metal = input("Enter a transition metal (e.g., W, Mo): ").strip()
    chalcogen = input("Enter a chalcogen (e.g., Se, S, Te): ").strip()

    supercell_x = int(input("Enter supercell size along x (e.g., 1, 2): ").strip())
    supercell_y = int(input("Enter supercell size along y (e.g., 1, 2): ").strip())
    supercell_z = int(input("Enter supercell size along z (e.g., 1, 2): ").strip())
    output_name = input("Enter output filename prefix (e.g., TMD_structure): ").strip()

    # Generate the TMD structure
    create_tmd_structure(metal=metal, chalcogen=chalcogen, size=(supercell_x, supercell_y, supercell_z), output_name=output_name)

