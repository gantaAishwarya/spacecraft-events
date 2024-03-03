#include <cmath>
#include <iostream>
#include <string>
#include <tuple>

class SpaceObject {
   protected:
    std::string name;

   public:
    explicit SpaceObject(const std::string& name) : name(name) {}

    auto get_name() const -> std::string { return name; }
};

class Orbit {
   private:
    double semi_major_axis;
    double eccentricity;

   public:
    Orbit(double semi_major_axis, double eccentricity)
        : semi_major_axis(semi_major_axis), eccentricity(eccentricity) {}

    auto get_semi_major_axis() const -> double { return semi_major_axis; }

    auto get_eccentricity() const -> double { return eccentricity; }
};

class Satellite : public SpaceObject {
   private:
    double x, y, z;
    Orbit orbit;

   public:
    Satellite(const std::string& name, double x, double y, double z,
              double semi_major_axis, double eccentricity)
        : SpaceObject(name),
          x(x),
          y(y),
          z(z),
          orbit(semi_major_axis, eccentricity) {}

    auto set_position(double new_x, double new_y, double new_z) {
        x = new_x;
        y = new_y;
        z = new_z;
    }

    auto get_position() const -> std::tuple<double, double, double> {
        return std::make_tuple(x, y, z);
    }

    auto distance_to(const Satellite& other) const -> double {
        double dx = x - other.x;
        double dy = y - other.y;
        double dz = z - other.z;
        return std::sqrt(dx * dx + dy * dy + dz * dz);
    }

    auto get_orbit() const -> const Orbit& { return orbit; }
};

int main() {

    //Defining two satellite instances
    Satellite satellite1("Satellite1", 100, 200, 300, 400, 0.1);
    Satellite satellite2("Satellite2", -50, 300, -100, 500, 0.3);

    // Printing satellite1 details
    std::cout << "Satellite 1 Details:" << std::endl;
    std::cout << "Satellite Name: " << satellite1.get_name() << std::endl;
    std::cout << "Satellite Position: " << std::get<0>(satellite1.get_position()) << ", "
              << std::get<1>(satellite1.get_position()) << ", "
              << std::get<2>(satellite1.get_position()) << std::endl;
    std::cout << "Orbit Semi-Major Axis: " << satellite1.get_orbit().get_semi_major_axis() << std::endl;
    std::cout << "Orbit Eccentricity: " << satellite1.get_orbit().get_eccentricity() << std::endl;


    // Printing satellite2 details
    std::cout << "\nSatellite 2 Details:" << std::endl;
    std::cout << "Satellite Name: " << satellite2.get_name() << std::endl;
    std::cout << "Satellite Position: " << std::get<0>(satellite2.get_position()) << ", "
            << std::get<1>(satellite2.get_position()) << ", "
            << std::get<2>(satellite2.get_position()) << std::endl;
    std::cout << "Orbit Semi-Major Axis: " << satellite2.get_orbit().get_semi_major_axis() << std::endl;
    std::cout << "Orbit Eccentricity: " << satellite2.get_orbit().get_eccentricity() << std::endl;

    // Printing distance between the two satellites
    std::cout << "\nDistance between satellites: " << satellite1.distance_to(satellite2) << std::endl;

    return 0;
}

