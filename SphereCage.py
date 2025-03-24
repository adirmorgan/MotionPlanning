def PlanR3(display_solution=True):    # Sphere in cage example
    pass

def buildEnv():
    pass


if __name__ == "__main__":
    obstacle_sphere_locations = {
        {0.55, 0, 0.25},
        {0.35, 0.35, 0.25},
        {0, 0.55, 0.25},
        {-0.55, 0, 0.25},
        {-0.35, -0.35, 0.25},
        {0, -0.55, 0.25},
        {0.35, -0.35, 0.25},
        {0.35, 0.35, 0.8},
        {0, 0.55, 0.8},
        {-0.35, 0.35, 0.8},
        {-0.55, 0, 0.8},
        {-0.35, -0.35, 0.8},
        {0, -0.55, 0.8},
        {0.35, -0.35, 0.8},
    }

    obstacle_sphere_radius = 0.2

    problem_env = buildEnv()
    PlanR3()