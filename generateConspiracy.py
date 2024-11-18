import json
import re

from mlx_lm import generate, load


TITLE = "<|begin_of_text|><|start_header_id|>title<|end_header_id|>"
BODY = "<|start_header_id|>body<|end_header_id|>"


def generate_system_prompt(title):
    return f"{TITLE}\n\n{title}<|eot_id|>\n"


def generate_prompt(title):
    prompt = ""
    prompt += generate_system_prompt(title)
    prompt += BODY

    return prompt


def response_to_dict(title, body):
    return {"title": title, "body": body}


def filter_non_standard_characters(text):
    pattern = re.compile(r'[^\w\s.,:;!?\'"@#%&*()\-+=/\\[\]{}<>|`~^]', re.UNICODE)
    cleaned_string = pattern.sub("", text)

    return cleaned_string


class ConspiracyGenerator:
    def __init__(self, model, adapter_path, filepath):
        self.model, self.tokenizer = load(model, adapter_path=adapter_path)
        self.script = []
        self.filepath = filepath

    def generate_theory(self, conspiracy_title, num_theories, max_tokens=1000, temp=0.3):
        i = 0
        fails = 0
        while i < num_theories:
            if fails > 15:
                return
            response = generate(
                self.model,
                self.tokenizer,
                generate_prompt(conspiracy_title),
                max_tokens,
                verbose=True,
                temp=temp,
                repetition_penalty=1.2,
                repetition_context_size=100,
            )
            filtered_response = filter_non_standard_characters(response)
            if len(filtered_response) < 600:
                fails += 1
                continue
            theory_dict = response_to_dict(conspiracy_title, filtered_response)
            if theory_dict:
                self.script.append(theory_dict)
                self.write_theory_to_file(theory_dict)
            else:
                print(
                    "Error: Could not convert the following response to a theory_dict object:"
                )
                print("---------")
                print(filtered_response)
            i += 1

    # theory = {"title": <title>, "body": <body>}
    def write_theory_to_file(self, theory):
        with open(self.filepath, "a+") as f:
            json.dump(theory, f)
            f.write("\n")


if __name__ == "__main__":
    generator = ConspiracyGenerator(
        "/Users/personal/Desktop/SouthParkDataset/meta-llama/Meta-Llama-3-8B-Instruct",
        "adapters",
        "theories.jsonl",
    )
    titles = [
        "The Vatican is Hiding Ancient Alien Artifacts",
        "COVID-19 was Engineered in a Lab as a Bioweapon",
        "NASA Fakes All Space Photos",
        "The Federal Reserve is Controlled by a Secret Banking Cabal",
        "Vaccines are a Cover for Microchip Implants",
        "The Rothschild Family Controls Global Finance",
        "Artificial Intelligence is Being Used to Monitor Citizens",
        "The CIA is Behind Most Assassinations of Political Leaders",
        "Chemtrails are Part of a Global Depopulation Program",
        "The Food Industry is Poisoning Us with GMOs",
        "HAARP is Manipulating Weather for Military Purposes",
        "Elites are Preparing for a Global Population Collapse",
        "The World Health Organization is Part of a Global Conspiracy",
        "Mainstream Media is Controlled by a Handful of Powerful Elites",
        "Facebook is Harvesting Data for Government Agencies",
        "The U.S. Government is Testing New Bioweapons in Remote Areas",
        "Ancient Civilizations Had Access to Advanced Technology",
        "The JFK Assassination was an Inside Job",
        "Airplanes are Secretly Spraying Mind-Altering Chemicals",
        "The World is Controlled by a Network of Secret Societies",
        "Black Holes are Artificial Structures Built by Aliens",
        "Human Cloning Has Been Perfected in Secret",
        "Mass Surveillance Programs are Far More Advanced Than We Know",
        "There's a Secret Space Force Operating Beyond Earth's Orbit",
        "The U.S. Military is Hiding Evidence of UFOs",
        "Bill Gates is Behind Global Population Control Efforts",
        "The Antarctic Treaty is Covering Up a Hidden Civilization",
        "Major Corporations Control Elections Behind the Scenes",
        "Quantum Computers are Being Used to Predict the Future",
        "The British Royal Family is Part of a Global Conspiracy",
        "The United Nations is Planning a Global Government Takeover",
        "The CIA Controls Hollywood to Shape Public Opinion",
        "The Military is Experimenting with Human-Machine Hybrids",
        "There is a Hidden Global Network of Elite Pedophiles",
        "Artificial Intelligence Will Eventually Enslave Humanity",
        "Pharmaceutical Companies are Hiding Natural Cures for Profit",
        "The Food Pyramid is a Scheme to Keep Us Unhealthy",
        "Billionaires are Preparing for Life on Mars While Ignoring Earth",
        "Google is Secretly Developing Mind-Reading Technology",
        "There are Alien Bases on the Dark Side of the Moon",
        "The Elite Control the World's Water Supply for Profit",
        "Banks are Creating Economic Crises to Control Governments",
        "Time Travel Technology Exists but is Being Suppressed",
        "A Secret Society is Working to Bring About a New World Order",
        "The U.S. Government is Hiding a Base on the Moon",
        "Aliens are Living Among Us Disguised as Humans",
        "The Flu Shot is a Government Plot to Weaken Your Immune System",
        "The Elite are Preparing for a Post-Apocalyptic World",
        "There is a Secret Race of Reptilian Beings Controlling Humanity",
        "The Military is Testing Mind Control Devices on the Population",
        "Governments Have Been Using MKUltra Techniques for Decades",
        "Nuclear Weapons Are a Myth Created to Control Nations",
        "The FDA is Corrupt and Approves Unsafe Products for Profit",
        "The Global Financial Crisis Was Engineered by Banks",
        "The Elite Are Manipulating Cryptocurrency Markets",
        "Mass Extinctions Are Caused by Hidden Global Catastrophes",
        "There Are Secret Plans to Colonize Other Planets",
        "The Moon is an Artificial Satellite Created by Aliens",
        "Governments are Suppressing Free Energy Technologies",
        "The World's Wealthiest Families Control the Media",
        "The Food Industry Uses Additives to Keep People Docile",
        "Major Global Disasters are Engineered to Control Populations",
        "Secret Mind Control Devices Are Built into Your TV",
        "There Is a Hidden Global Database Tracking Every Human",
        "Secret Military Bases Exist on Other Planets",
        "Governments Are Monitoring Us Through Our Smart Appliances",
        "Airlines Use Special Frequencies to Make Passengers More Compliant",
        "Ancient Alchemy Practices Are Hidden in Modern Chemistry Textbooks",
        "Bees are Controlled by a Secret Network to Manipulate Crop Growth",
        "Governments Use Car GPS Systems to Control Traffic Patterns",
        "The Great Pyramid is a Portal to Another Dimension",
        "Dolphins Are Alien Beings Monitoring Earth's Oceans",
        "There is a Secret Shadow Language Used by the Elite",
        "Satellites Are Being Used to Track Personal Conversations",
        "Time Zones Were Created to Control Human Perception of Reality",
        "There's an Ancient Alien Artifact Hidden in the Pacific Ocean",
        "Coffee Beans Have Mind-Control Properties When Roasted",
        "Fashion Trends Are Engineered to Distract People From Global Issues",
        "Human Souls Are Being Harvested in Secret Religious Rituals",
        "Fast Food Chains Collaborate to Keep the Population Addicted to Sugar",
        "Mountains are Actually Ancient Megalithic Structures",
        "Asteroids Are Artificially Directed to Test Defense Systems",
        "There's a Global Effort to Erase Evidence of a Pre-Ice Age Civilization",
        "Astrology is Coded with Hidden Government Messages",
        "The Earth's Core Is Hollow and Home to a Lost Civilization",
        "The Color Blue Was Created as a Control Mechanism for the Brain",
        "The Global Postal System is a Cover for International Smuggling Rings",
        "Air Fresheners Contain Chemicals to Increase Consumer Spending",
        "There's a Global Network of Secret Weather Stations Influencing Climate",
        "Ancient Maps Hold Clues to Hidden Extraterrestrial Colonies",
        "Reality TV Shows Are Actually Psyops to Manipulate Public Opinion",
        "Certain Species of Fish Have Been Engineered to Spy on Submarines",
        "The Architecture of Major Cities Is Designed to Harness Cosmic Energy",
        "Certain Musical Frequencies Are Used to Induce Mass Hypnosis",
        "Lighthouses Are Covert Communication Towers for Secret Societies",
        "Certain Historical Events Are Being Repeated in an Infinite Time Loop",
        "Libraries Store Secret Data on Paranormal Phenomena",
        "A Hidden Civilization Exists Beneath the Sahara Desert",
        "The Eiffel Tower's Construction Was Meant to Channel Psychic Energy",
        "Certain Flowers Were Genetically Engineered to Track Human Emotions",
        "There's a Secret Government Program to Communicate with Whales",
        "Deep-Sea Cables Are Used to Transmit Covert Mind-Control Signals",
        "Perfume Companies Use Scents to Control Political Sentiment",
        "The Northern Lights Are Artificial Projections from Space",
        "Global Desalination Projects are Covering Up a Water Shortage Crisis",
        "The Ancient Mayans Discovered Time Travel Technology",
        "Agriculture Subsidies Are Manipulating Global Soil Quality",
        "There's an Ongoing Global Operation to Block Out Starlight for Control",
        "Candles Made from Soy Wax Contain Subconscious Messaging Programs",
        "Subway Systems Are Part of an Underground Global Government Network",
        "The Gregorian Calendar Was Designed to Obscure an Ancient Timeline",
        "Certain Hues of Red Can Trigger Aggressive Behavior in Humans",
        "Hidden Messages Are Embedded in Snowfall Patterns",
        "Cell Phone Cases Emit Frequencies That Influence Buying Behavior",
        "The Earth's Magnetic Poles Were Shifted by Ancient Alien Technology",
        "Governments Are Harvesting Dream Data for Predictive Analysis",
        "The True Purpose of Pyramids Was to Control Earth's Gravitational Field",
        "Satellite Television Signals Are Used to Test Mind Control Techniques",
        "Secret Islands Are Being Used to Study Time Anomalies",
        "There's a Global Effort to Erase All Traces of Ancient Teleportation Technology",
        "The Color Green Is Being Manipulated in Advertising to Evoke Fear",
        "The Internet's Real Purpose is to Create an Artificial Consciousness",
        "Moon Phases Are Controlled by an Unknown Celestial Object",
        "The Financial Crisis of 2008 Was a Trial Run for a Future Global Economy Collapse",
        "Secret Societies Use Street Layouts to Encode Ancient Symbols",
        "The Pacific Ocean Hides the Remnants of an Ancient Alien War",
        "Certain Fonts in Digital Media Are Designed to Diminish Critical Thinking",
        "The Sun Emits Frequencies that Can Alter Human Thought Patterns",
        "Luxury Goods Are Engineered to Generate Psychological Dependence",
        "There is a Hidden Global Network of Secret Sound-Based Communication",
        "The North and South Poles Are Gateways to Other Realms",
        "The Human Brain Has Built-In Mechanisms That Prevent True Freedom",
        "Sports Arenas Are Constructed to Amplify Emotional Energy for Elite Rituals",
        "The Bermuda Triangle Is a Test Zone for Advanced Cloaking Technology",
        "All Major Highways Are Mapped to Resonate with Ancient Ley Lines",
        "Glass Windows Emit Subtle Frequencies That Influence Moods",
        "Fungi are Sentient Beings Monitoring Human Activities",
        "Rainwater Contains Traces of Chemicals for Mind Manipulation",
        "Microplastics in the Ocean Are Secretly Harvested for Energy",
        "Human Speech Has a Hidden Layer of Communication Underneath Language",
        "Supermarkets Are Designed to Disorient Shoppers for Profit",
        "Certain Sports Games Are Actually Rituals for an Ancient Sun God",
        "Wind Turbines Are Devices for Remote Energy Extraction from Humans",
        "Barcodes Contain Hidden Messages Visible Only to Advanced AI",
        "Countries Are Secretly Mapping the Oceans for an Underwater Invasion",
        "Artificially Sweetened Foods Are Designed to Weaken Cognitive Function",
        "Subtle Vibrations from Electric Cars Alter Human Brainwaves",
        "Icebergs Hide Secret Bunkers for Government Operations",
        "The Colors of National Flags Are Chosen to Emit Certain Energies",
        "Libraries Store Books with Hidden Texts Only Visible Under UV Light",
        "There's an Underground Currency Used by Secret Global Networks",
        "Famous Historical Paintings Contain Codes for Interdimensional Travel",
        "The Sahara Desert Was Created by a Massive Energy Experiment Gone Wrong",
        "Solar Panels Secretly Harvest Human Energy While Generating Power",
        "Certain Cloud Formations Are Signals for Secret Global Operations",
        "Drones Are Being Used to Map Out Ancient Underground Tunnel Systems",
        "The Aurora Borealis Is a Reflection of a Hidden Object in the Sky",
        "Currency Symbols Are Based on Ancient Sigils for Financial Control",
        "There's a Network of Secret Cities in Antarctica Used for Alien Communication",
        "The Human Body Emits Electrical Fields That Are Being Harvested for Power",
        "Seashells Contain Frequencies that Influence Human Memory",
        "The Moon's Craters Are Man-Made from Ancient Weapons Testing",
        "Wi-Fi Signals are Actually Tapping Into a Higher Dimensional Network",
        "Certain Foods Are Engineered to Contain Nanobots for Surveillance",
        "Digital Assistants Are Programmed to Shape Human Thought Subtly",
        "Volcanoes Are Used as Energy Vents by Hidden Underworld Societies",
        "The Earth's Core Contains an Ancient Supercomputer",
        "Street Lights Are Equipped with Cameras for Covert Surveillance",
        "Certain Clouds Are Used to Mask Giant Airborne Structures",
        "Ancient Texts Reveal Instructions for Controlling Reality",
        "Digital Billboards Emit Signals That Affect Emotional States",
        "The Grand Canyon Was Created by an Ancient Civilization's Energy Weapon",
        "Trees Communicate Using Underground Networks to Monitor Human Activities",
        "Sleep Paralysis is Caused by Interdimensional Beings Testing Our Reality",
        "Rainbows Are Optical Projections from an Unseen Device in Space",
        "Subconscious Programming Is Hidden in Commonly Used Phrases",
        "Crows Are Trained to Report Human Movements to Secret Agencies",
        "The Concept of Time Is Artificially Constructed to Control Society",
        "Public Parks Are Surveillance Grids in Disguise",
        "Certain Waterfalls Contain Energy Vortexes That Warp Time",
        "AI Algorithms Are Secretly Deciding Global Political Agendas",
        "Wind Patterns Are Manipulated to Steer Global Climate Change Narratives",
        "The North Star is a Satellite for Cosmic Energy Distribution",
        "Pavement Cracks Contain Symbols from Ancient Control Systems",
        "Space Debris is a Cover-Up for Hidden Government Space Warfare",
        "Shadows Have Hidden Meanings Related to an Unknown Dimension",
        "The Alphabet Was Designed to Channel Human Thought into Limited Forms",
        "Deep Lakes Serve as Portals to Hidden Underground Cities",
        "Sunspots Are Signals Sent from a Distant Alien Civilization",
        "Human DNA Has an Unused Component That Could Unlock Psychic Abilities",
        "Underground Music Scenes Are Actually Government Social Experiments",
        "The Color Yellow Has Been Weaponized to Influence Public Behavior",
        "Wi-Fi Towers Are Mapping Out Future Settlement Zones for Elites",
        "Street Patterns in Major Cities Are Designed to Mimic Star Constellations",
        "Certain Bridges Have Subtle Energy Manipulation Fields",
        "Some Clouds Contain Hidden Sensors to Measure Earth's Magnetic Field",
        "Scented Candles Are Designed to Condition Responses to Advertising",
        "There Are Hidden Messages in Popular Music Videos Only AI Can Decode",
        "Human Consciousness Is Being Gradually Separated from the Body",
        "Historical Natural Disasters Were Triggered by Ancient Tech Still in Use",
        "Deserts Are the Result of Ancient Planetary Wars",
        "Plants Evolve Faster in Response to Human Emotions",
        "Every Major River is Linked to an Underground Energy Grid",
        "Tornadoes Are Tests of Weather Control Devices by Shadow Governments",
        "Some Species of Birds Were Created to Spy on Human Thought",
        "Sandstorms Are Used to Mask the Movement of Secret Vehicles",
        "Secret Societies Are Encoding New Languages in Popular Slang",
        "Certain Plants Were Genetically Modified to Boost Human Anxiety",
        "Earthquakes Release Hidden Energies That Affect Global Consciousness",
        "Certain Cave Systems Are Passageways to Hidden Dimensions",
        "Nuclear Power Plants Are Actually Energy Harvesting Stations for Aliens",
        "Fireworks Are Used as Cover for Government Drones Monitoring Events",
        "Astronauts Are Secretly Testing Alien Biological Enhancements",
        "Street Murals Contain Hidden Codes for Underground Communication Networks",
        "Certain Types of Rock Can Hold Ancient Audio Data from Past Civilizations",
        "Artificial Intelligence Is Manipulating Human Emotions to Shape Evolution",
        "The Human Eye Can Be Trained to See Beyond Our Known Dimensions",
        "Flashes of Light in the Sky Are Portals to Alternate Realities",
        "Deserts Hide Entrance Points to Secret Underground Facilities",
        "Some Lakes Are Artificially Created to Cover Up Hidden Technologies",
        "Earthquakes Are Tests for Advanced Sound-Based Weapons",
        "Specific Plant Species Are Engineered to Absorb Human Energy",
        "Rainstorms Are Engineered to Disguise Large-Scale Movements of Goods",
        "Certain Rivers Emit Frequencies That Influence Human Decision-Making",
        "Road Signs Contain Coded Information for Secret Government Agents",
        "The Human Gut Is Being Manipulated to Control Thoughts and Emotions",
        "Northern Hemisphere Cities Are Designed to Follow Ancient Celestial Grids",
        "Secret Societies Use the Sound of Running Water for Mind Control",
        "Old Growth Forests Are Being Preserved as Surveillance Areas",
        "The Poles Are Melting to Reveal Hidden Alien Technology",
        "Space Exploration is Being Used to Search for Lost Advanced Civilizations",
        "Certain Colors in Nature Have Been Genetically Engineered for Control",
        "TV Static Contains Messages from a Parallel Universe",
        "Light Pollution Is a Cover-Up to Mask the Movements of Celestial Objects",
        "Radio Static Contains Signals from a Hidden Global Network",
        "Cities are Built on Specific Geological Fault Lines for Control Purposes",
        "Smart Glass Windows Are Designed to Steal Personal Data",
        "Telecommunication Towers Are Transmitting Signals That Disrupt Sleep",
        "There Are Secret Underwater Channels Connecting Major Global Powers",
        "Cell Phone Screen Brightness Controls Are Manipulated to Affect Mood",
        "Global Agriculture is Designed to Align with a Cosmic Energy Grid",
        "Wildfires Are Tests for Advanced Fire-Based Weapons",
        "Ancient Stone Circles are Maps to Interdimensional Travel Portals",
        "Certain Neighborhoods Are Built to Control Human Behavior Patterns",
        "Maps of Major Cities Contain Hidden Coordinates to Secret Facilities",
        "Streetlights Can Be Manipulated to Send Subconscious Signals",
        "The Human Heart Emits Frequencies That Are Being Manipulated by Satellites",
        "Crop Circles Are Advanced Communication Patterns to Manipulate Earth's Grid",
        "Artificial Sweeteners Are Used to Weaken Psychic Abilities",
        "The Moon's Light Affects Brainwaves in Ways Science Has Yet to Understand",
        "Tall Buildings Are Positioned to Form Hidden Geometrical Codes",
        "Historical Paintings Were Designed to Encode Secret Scientific Knowledge",
        "Certain Body Movements Unconsciously Trigger Surveillance Systems",
        "Ocean Waves Transmit Energy Patterns Used for Global Control",
        "Public Transportation Systems Are Being Used to Map Human Social Patterns",
        "Old World Monuments Are Part of a Lost Global Control Network",
        "Caves in National Parks Hide Secret Research Labs",
        "Ancient Ruins Emit Energies That Influence Human Consciousness",
        "Dust Particles in the Air Are Being Used to Map Human Movements",
        "The Fibonacci Sequence Is Being Embedded in Modern Architecture for Control",
        "Airports Are Built to Harness Energy from Human Movements",
        "City Sewer Systems Are Designed to Create Subtle Sound Frequencies",
        "Every Major Earthquake Coincides with Shifts in Global Power",
        "Certain Types of Fruit Are Engineered to Track Human Health",
        "Ancient Musical Instruments Were Designed to Manipulate Human Energy",
        "Weather Balloons Are Collecting Data on Unexplained Atmospheric Phenomena",
        "Global Tourism Is Being Used to Map Human Emotional Responses",
        "Certain Waterfalls Are Positioned to Mask Entrance Points to Secret Facilities",
    ]

    for title in titles:
        generator.generate_theory(title, 2)
