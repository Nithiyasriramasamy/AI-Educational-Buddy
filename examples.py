"""
Example teaching scripts for AI Teaching Video Generator
"""

EXAMPLE_SCRIPTS = {
    "photosynthesis": {
        "title": "Introduction to Photosynthesis",
        "script": """First, let's understand what photosynthesis is. Photosynthesis is the process by which plants convert sunlight into energy. This amazing process is essential for life on Earth.

Next, we'll explore the key components needed for photosynthesis. Plants need three main things: sunlight, water, and carbon dioxide. These ingredients work together in a special way.

Now, let's look at what happens during photosynthesis. The chloroplasts in plant leaves capture sunlight and use it to convert water and carbon dioxide into glucose and oxygen. This happens in two main stages.

Finally, we'll discuss why photosynthesis is important. This process not only feeds the plant but also produces the oxygen we breathe. Without photosynthesis, life as we know it wouldn't exist."""
    },
    
    "math_fractions": {
        "title": "Understanding Fractions",
        "script": """Let's start by understanding what a fraction represents. A fraction shows us parts of a whole. The top number is called the numerator, and the bottom number is called the denominator.

For example, if we have a pizza cut into 8 slices and we eat 3 slices, we can represent this as the fraction 3/8. The 3 represents the parts we took, and the 8 represents the total parts.

Next, let's learn about equivalent fractions. Different fractions can represent the same amount. For instance, 1/2 is the same as 2/4 or 4/8. We can find equivalent fractions by multiplying or dividing both the numerator and denominator by the same number.

Now we'll practice adding fractions. When fractions have the same denominator, we simply add the numerators. For example, 1/4 + 2/4 = 3/4. When denominators are different, we need to find a common denominator first.

Finally, let's see how fractions are used in real life. We use fractions when cooking, measuring, telling time, and in many other daily activities. Understanding fractions helps us solve practical problems."""
    },
    
    "solar_system": {
        "title": "Our Solar System",
        "script": """Welcome to our journey through the solar system. Our solar system consists of the Sun and all the objects that orbit around it, including planets, moons, asteroids, and comets.

First, let's meet our star, the Sun. The Sun is a massive ball of hot gas that provides light and heat to our entire solar system. It's so large that over one million Earths could fit inside it.

Moving outward from the Sun, we encounter the inner planets. Mercury, Venus, Earth, and Mars are called terrestrial planets because they have solid, rocky surfaces. Earth is the only planet we know of that supports life.

Next, we explore the outer planets. Jupiter, Saturn, Uranus, and Neptune are gas giants, much larger than the inner planets. Jupiter is the largest planet, and Saturn is famous for its beautiful rings.

Finally, let's discuss what makes our solar system special. The perfect distance from the Sun allows Earth to have liquid water, and the gravitational forces keep everything in stable orbits. Our solar system is just one of billions in the universe."""
    },
    
    "water_cycle": {
        "title": "The Water Cycle",
        "script": """Today we'll learn about the water cycle, the continuous movement of water on, above, and below Earth's surface. This process has been happening for billions of years.

First, let's understand evaporation. When the Sun heats water in oceans, lakes, and rivers, it turns into invisible water vapor that rises into the atmosphere. Plants also release water vapor through their leaves in a process called transpiration.

Next, we'll explore condensation. As water vapor rises higher in the atmosphere, it cools down and forms tiny water droplets around dust particles. These droplets cluster together to form clouds.

Now let's see what happens with precipitation. When water droplets in clouds become too heavy, they fall back to Earth as rain, snow, sleet, or hail. This brings fresh water back to the surface.

Finally, we'll follow the water's journey back to the ocean. Some precipitation flows over the ground as runoff, eventually reaching rivers and streams. Some soaks into the ground as groundwater. All of this water eventually makes its way back to the oceans, where the cycle begins again."""
    },
    
    "programming_basics": {
        "title": "Introduction to Programming",
        "script": """Let's begin our journey into programming. Programming is the process of creating instructions for computers to follow. These instructions are written in special languages that computers can understand.

First, we need to understand what an algorithm is. An algorithm is a step-by-step procedure for solving a problem. Just like following a recipe to bake a cake, computers follow algorithms to complete tasks.

Next, let's explore variables and data types. Variables are like containers that store information. We can store different types of data like numbers, text, or true/false values. Each type of data has specific rules for how it can be used.

Now we'll learn about control structures. These include loops, which repeat actions, and conditionals, which make decisions. For example, we might tell a computer to repeat an action 10 times, or to do something only if a certain condition is true.

Finally, let's see why programming is important. Programming skills help us solve problems, automate tasks, and create amazing applications. From websites to video games to scientific research, programming powers the modern world."""
    }
}

def get_example_script(example_name: str) -> str:
    """Get an example script by name"""
    if example_name in EXAMPLE_SCRIPTS:
        return EXAMPLE_SCRIPTS[example_name]["script"]
    return ""

def list_examples() -> list:
    """List all available example scripts"""
    return [
        {
            "name": name,
            "title": data["title"],
            "preview": data["script"][:100] + "..."
        }
        for name, data in EXAMPLE_SCRIPTS.items()
    ]

def get_random_example() -> dict:
    """Get a random example script"""
    import random
    name = random.choice(list(EXAMPLE_SCRIPTS.keys()))
    return {
        "name": name,
        "title": EXAMPLE_SCRIPTS[name]["title"],
        "script": EXAMPLE_SCRIPTS[name]["script"]
    }