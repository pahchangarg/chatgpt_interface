import jellyfish
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
nltk.download('punkt')

def compute_jaccard_similarity(paragraph1, paragraph2):
    # Tokenize the paragraphs into words
    words1 = set(word_tokenize(paragraph1.lower()))
    words2 = set(word_tokenize(paragraph2.lower()))

    # Calculate the Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    jaccard_similarity = intersection / union

    return jaccard_similarity

def compute_euclidean_distance(paragraph1, paragraph2):
    # Tokenize the paragraphs into words
    words1 = word_tokenize(paragraph1.lower())
    words2 = word_tokenize(paragraph2.lower())

    # Create a combined set of unique words
    unique_words = sorted(set(words1 + words2))

    # Create vectors for the paragraphs
    vector1 = [words1.count(word) for word in unique_words]
    vector2 = [words2.count(word) for word in unique_words]

    # Compute the Euclidean distance between the vectors
    euclidean_distance = euclidean_distances([vector1], [vector2])[0][0]

    return euclidean_distance

def compute_cosine_similarity(paragraph1, paragraph2):
    # Combine the paragraphs into a single list
    paragraphs = [paragraph1, paragraph2]

    # Initialize the TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Compute the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(paragraphs)

    # Compute the cosine similarity between the paragraphs
    similarity_matrix = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])

    # Extract the cosine similarity value
    similarity = similarity_matrix[0][0]

    return similarity

def compute_jaro_winkler_distance(paragraph1, paragraph2):
    # Split paragraphs into lines
    lines1 = paragraph1.splitlines()
    lines2 = paragraph2.splitlines()

    # Initialize variables for total distance and line count
    total_distance = 0
    line_count = 0

    # Iterate over each line in the first paragraph
    for line1 in lines1:
        line_distances = []

        # Iterate over each line in the second paragraph
        for line2 in lines2:
            # Compute Jaro-Winkler distance between the lines
            distance = jellyfish.jaro_winkler(line1, line2)
            line_distances.append(distance)

        if line_distances:
            # Find the highest Jaro-Winkler distance for the line
            max_distance = max(line_distances)
            total_distance += max_distance
            line_count += 1

    # Calculate the average Jaro-Winkler distance
    if line_count > 0:
        average_distance = total_distance / line_count
        return average_distance
    else:
        return 0

# origRequirements = """
# As a Data Publishing User, I want to be able to edit a dataset I have published, So that I can correct or enhance existing data.
# As a Data Publishing User, I want to be able to edit the model of data I have already imported, So that I can fix bugs or make enhancements in the API built for my data.
# As a Data Publishing User, I want to be able to delete a dataset I have published, So that I can remove unwanted data from OpenSpending.
# As a Platform Administrator, I want to be able to Hide any dataset already added as Public, So that I can maintain Public/Hidden status for other users.
# As a Platform Administrator, I want to have a view on all datasets published by all users, So that I can perform management actions on any dataset.
# As a Platform Administrator, I want to be able to delete any dataset published, So that I can deal with takedown requests, or clean up test datasets.
# As a Data Publishing User, I want to be able to edit the data source of data I have already imported, So that I can fix bugs or make enhancements in the API built for my data.
# As a Data Publishing User, I want to have the Packager support Constants, So that I can model dimensions that may not exist in the source file.
# As a Data Publishing User, I want to be able to import data in Excel, So that I do not have to convert data formats in order to use the data packager.
# As a Data Publishing User, I want to know what my data needs to be able to be visualised on a map, So that I can visualise it on a map.
# As a Data Publishing User, I want to be able to import data in JSON, So that I do not have to convert data formats in order to use the data packager.
# As a Data Publishing User, I want to be able to import data from a Google Spreadsheet, So that I do not have to convert data formats in order to use the data packager.
# As a Data Publishing User, I want to be able to import data from Fiscal Data Package descriptor file, So that I do not have to convert data formats in order to use the data packager.
# As a Data Publishing User, I want to be able to provide the Platform Administrator with additional GeoJSON sources, So that I can improve the map-based visualisations of my data.
# As a Data Consuming User, I want to be able to filter, sort and aggregate data by multiple dimensions and measures, So that I can get more granular views on the data.
# As a Data Consuming User, I want to be able to download a CSV of the data that is used in any visualisation I am viewing, So that I can use the data in other tools.
# As a Data Consuming User, I want to be able to change the display of all monetary measures across a set of currencies, So that I can understand localised amounts in non-localised figures.
# As a Data Consuming User, I want to see textual descriptions that accompany embedded visualisations, So that I can more easily understand what I am viewing.
# As a Data Consuming User, I want to be able to share a view state as a URL to social networks, So that I can share data that I have found with others.
# As a Data Consuming User, I want to be able to download an image ofa particular view state, So that I can use it offline.
# As a Data Consuming User, I want to be able to share an image of a particular view state to the social networks that support this, So that I can provide richer context in those communication channels for data I am sharing.
# As a Data Consuming User, I want to be able to have stepped zoom on map visualisations, So that I can have better control over the navigation experience inside a map view.
# As a Data Consuming User, I want to have consistent use of colour on map visualisations, So that I can better understand the visual logic of the map view.
# As a Developer, I want to be able to customise the Brand Name and Icon, and Primary Color of all frontend Javascript apps, So that I can customise the branding for my own needs.
# As an API User, I want to be able to understand if a user is a Publisher, So that I can offer functionality based on Dataset Publisher privileges.
# As an API User, I want to be able to understand if a user is an Administrator, So that I can offer functionality based on Platform Administration privileges.
# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.
# As an API User, I want to be able to dynamically request polygons based on the query made, So that I can provide maps that match the query.
# As an API User, I want to have a flexible API using HASC codes for countries, regions and cities, So that I can visualise budget data on maps.
# As an API User, I want to be able to get a CSV output of any cube-based query, So that I can use work with tools that read CSV.
# As an API User, I want to be able to get a set of monetary measures transferred to different currencies, So that I can use this in scenarios that might enable comparison by normalisation.
# As an API User, I want to be able to use metadata to get results from multiple datasets, So that I can build user experiences based on more than one dataset more easily.
# As an API User, I want to be able to use data to get results from multiple datasets, So that I can build user experiences based on more than one dataset more easily.
# As an API User, I want to be able to normalise measures by population, So that I work with datasets in reference to their contextual constraints.
# As an API User, I want to be able to normalise measures by geographical area, So that I work with datasets in reference to their contextual constraints.
# As an API User, I want to be able to normalise measures by GDP, so I work with datasets in reference to their contextual constraints.
# As an API User, I want to be able to normalise measures by GINI and related socioeconomic indexes, So that I work with datasets in reference to their contextual constraints.
# As an API User, I want to be able to get a relative percentage of a measure to the total of the dataset it comes from, So that I can build alternative displays of the data.
# As an API User, I want to be able to persistently store visualisation state in the database, So that such can be shared more easily and contribute to a visualisation gallery.
# As a Data Publishing User, I want to have my dataset update automatically as the source file/files changes, So that OpenSpending always shows current data.
# As an OpenSpending Community Member, I want to have a blog that highlights any and all projects in the open fiscal space, So that I can relate to openspending.org as the central hub of fiscal openness.
# As a User, I want to be able to set my own username, So that my data is more easily discoverable.
# As a Data Publishing User, I want to be able to add a dataset in a Hidden state, So that I can work on a dataset before having it discoverable via OpenSpending user interfaces.
# As a Data Publishing User, I want to be able to Hide a dataset that I have already added as Public, So that I can fix my mistakes or have a dataset primarily for my own use.
# As a Data Publishing User, I want to have a view on all the datasets I have published, So that I can perform management actions on my own datasets.
# As a Data Publishing User, I want to have a functioning Python Client, So that I can add data to the datastore in bulk from the command line or my own programs.
# As an OpenSpending Community Member, I want to have an app where I can find examples of use of fiscal data visualisations, So that I can find guidance in creating my own with Open Spending.
# As a Data Publishing User, I want to know if my CSV file is valid, So that I can fix possible data issues before publishing it on Open Spending.
# As a Data Consuming User, I want to be able to search any dataset published and publicly accessible by their title and metadata, So that I can find the datasets I'm interested in.
# As a Data Consuming User, I want to visualize by default in treemap, bubble tree, map and pivot table the most recent year when my dataset contain multiple years, So that I'm not confused with the amounts.
# As an API user, I want to be able to change the colors of the embedded visualisations in my own platform, So that I can customize the visualisations.
# As an API user, I want to be able to change some of the styling of the embedded Viewer in my own platform, So that I can brand it to my own organisation's color scheme.
# As a Platform administrator, I want to be able to translate the data types hierarchies of the Viewer while in embed mode, So that my users can understand the interface in their native language.
# """

# genRequirements1 = """
# As a Data Publishing User, I want to be able to easily edit, enhance, or correct existing datasets.
# As a Data Publishing User, I want the ability to edit the data source and model of my imported data.
# As a Data Publishing User, I want to be able to delete unwanted datasets.
# As a Data Publishing User, I want to provide additional GeoJSON sources for improved map-based visualizations.
# As a Platform Administrator, I want a comprehensive view of all published datasets.
# As a Platform Administrator, I want the ability to hide public datasets.
# As a Platform Administrator, I want to be able to delete any dataset as needed.
# As a Data Consuming User, I want to be able to filter, sort, and aggregate data.
# As a Data Consuming User, I want to be able to download CSV files.
# As a Data Consuming User, I want the ability to change display settings for monetary measures.
# As a Data Consuming User, I want to easily share visualizations and images.
# As a Developer, I want the flexibility to customize the branding and appearance of the frontend apps.
# As a Developer, I want to utilize the API to manage user privileges.
# As a Developer, I want to utilize the API to access bordering regions/cities.
# As a Developer, I want the API to support dynamic polygon requests.
# As a Developer, I want the API to provide CSV outputs.
# As a Developer, I want the API to support currency conversions.
# As a Developer, I want the API to allow accessing multiple datasets.
# As a Data Publishing User, I want the application to normalize measures automatically.
# As a Data Consuming User, I want the application to persist visual state across sessions.
# As a Data Publishing User, I want the application to provide automatic dataset updates.
# As a Data Publishing User, I want the application to have a blog highlighting projects.
# As a Data Publishing User, I want the ability to customize usernames.
# As a Developer, I want a Python client for bulk data addition.
# As a Data Publishing User, I want OpenSpending to be the central hub of fiscal openness.
# As a Data Publishing User, I want OpenSpending to provide a rich ecosystem for data publishers, consumers, and the OpenSpending community.
# """

# genRequirements = """
# As a Data Publishing User, I want to easily create and publish datasets for fiscal data.
# As a Data Publishing User, I want to edit existing datasets to correct any errors or enhance the data.
# As a Data Publishing User, I want the ability to edit the data source and model of imported datasets.
# As a Data Publishing User, I want to delete unwanted datasets from the application.
# As a Data Publishing User, I want to provide additional GeoJSON sources for improved map-based visualizations.
# As a Platform Administrator, I want a comprehensive view of all published datasets.
# As a Platform Administrator, I want the ability to hide public datasets when necessary.
# As a Platform Administrator, I want the ability to delete any dataset as needed.
# As a Data Consuming User, I want to filter datasets based on specific criteria.
# As a Data Consuming User, I want to sort datasets based on different attributes.
# As a Data Consuming User, I want to aggregate data from multiple datasets for analysis.
# As a Data Consuming User, I want to download datasets in CSV file format for further analysis.
# As a Data Consuming User, I want to change display settings for monetary measures, such as currency format or precision.
# As a Data Consuming User, I want to easily share visualizations and images generated from the application.
# As a Developer, I want the ability to customize the branding and appearance of the frontend apps.
# As a Developer, I want to access the API to implement user privileges for different functionalities.
# As a Developer, I want the ability to include bordering regions/cities in the application's geographical features.
# As a Developer, I want to make dynamic polygon requests to retrieve specific data based on geographical areas.
# As a Developer, I want the API to provide CSV outputs for easy data integration with other systems.
# As a Developer, I want to perform currency conversions within the application.
# As a Developer, I want to access multiple datasets through the API for comprehensive data analysis.
# As a Data Publishing User, I want the option to normalize measures within datasets for consistency.
# As a Data Publishing User, I want the application to automatically update datasets when new data becomes available.
# As a Data Publishing User, I want a blog feature to highlight projects and share insights related to fiscal data.
# As a Data Publishing User, I want customizable usernames to personalize my profile and dataset contributions.
# As a Data Publishing User, I want a Python client that allows bulk data addition to the application.
# As a Data Publishing User, I want the ability to provide metadata for datasets to improve searchability and understanding.
# As a Data Consuming User, I want the option to bookmark and save favorite datasets for easy access.
# As a Platform Administrator, I want to manage user roles and privileges within the application.
# As a Platform Administrator, I want to track and monitor user activity and dataset usage.
# As a Data Consuming User, I want the ability to generate visualizations based on selected datasets and filters.
# As a Data Consuming User, I want the option to export visualizations as images or embed them in external websites.
# As a Data Consuming User, I want the application to provide interactive data exploration tools, such as charts and graphs.
# As a Data Consuming User, I want to receive notifications or updates when new datasets are published or existing ones are updated.
# As a Developer, I want the API to provide documentation and examples for easy integration and usage.
# As a Developer, I want access to developer resources, including code samples and libraries, to support application customization.
# As a Data Publishing User, I want the ability to import datasets from external sources, such as CSV files or database connections.
# As a Platform Administrator, I want to perform backups and ensure data integrity and availability.
# As a Data Consuming User, I want to search for specific datasets based on keywords or tags.
# As a Developer, I want to access data versioning and revision history for datasets.
# As a Data Publishing User, I want the option to collaborate with other users on dataset creation and maintenance.
# As a Data Consuming User, I want the application to provide data summaries or key statistics for selected datasets.
# As a Platform Administrator, I want to generate usage reports and analytics to assess the application's performance and user engagement.
# As a Data Consuming User, I want the option to bookmark and save specific data views or filters for future reference.
# As a Developer, I want the API to support authentication and authorization mechanisms for secure access to data and functionalities.
# As a Data Publishing User, I want the ability to import data in different formats, such as JSON or XML.
# As a Platform Administrator, I want the application to provide data validation and quality checks for imported datasets.
# As a Data Consuming User, I want to compare data from different datasets side by side.
# As a Developer, I want the API to provide advanced querying capabilities, such as filtering based on date ranges or numeric conditions.
# As a Data Publishing User, I want the option to publish datasets in multiple languages to cater to a diverse user base.
# """

origRequirements = """
The MOSAR technology shall allow repair and update of modular spacecraft by manipulation and repositioning of functional modules with a robotic manipulator
The modular spacecraft shall be reconfigurable and should be able to use new functionalities brought by additional functional modules, in order to perform new mission tasks
The robotic manipulator shall be able to add and replace whole functional modules (ASM/APM) by using the interconnectors of these modules.
The robotic manipulator shall be able to reposition itself by using the interconnectors/structure of the functional modules or the spacecraft
A design software shall be able to create a robotic compatible servicing / reconfiguration plan for the modular spacecraft
A simulation software shall be able to simulate the system with all related robotics elements following the execution plan
The modular spacecraft shall perform the high-level control of the robot, by the execution and monitoring of the reconfiguration plan (task level)
The robotic manipulator shall ensure its low-level control for the execution of the high level tasks 
The modular spacecraft shall be able to monitor the status of essential parameters of each connected functional module
The system shall be able to reallocate resources (e.g. power, data, computational power, etc.) and assign different path automatically in case of a defect (e.g. interconnector of an APM)
The system shall be able to handle the tasks even during a connection failure or a power interruption of defect modules/interconnectors.
One or several modules options shall be available to implement for electrical power supply enabling operation of the functional modules and the robot manipulator
The modular spacecraft shall be able to shut down or command a stand-by mode of any non-critical module to reduce power consumption if needed. Critical functions should not be affected by shutting down of non-critical modules. 
One or several modules options shall be available to implement a data handling system (that can be composed of one or more modules) that enables operation of the different modules and the manipulator.
One or several modules options shall be available to implement heat management functions that allow thermal regulation of the different modules within its specific range of temperatures. The heat management system could be composed of one or more modules.
One or several modules options shall be available to implement a propulsion subsystem with capacity to perform at least: Station keeping manoeuvers; Orbit relocation; De-orbiting.
One or several modules options shall be available to implement an attitude control subsystem, with capacity to perform at least: Spacecraft reorientation; Attitude control compatible with mission objectives; Autonomous search of the Sun and the Earth
Modules shall be able to connect mechanically to other modules or to the spacecraft through interconnectors.
Any module should be able to act as a data relay for other modules or the robotic manipulator through their interconnector, also if the module is in safe mode
The OBC shall be able to redirect telecommands to specific modules, for the spacecraft configuration or for instance upon detection of failure on any point of the network. If an alternative path is not available, the OBC shall be able to isolate the faulty node and all the others nodes connected downstream.
Module should be able to act as a power relay for other modules or the robotic manipulator through their interconnectors, also if the module is in safe mode
The OBC shall be able to redirect power to specific modules, for the spacecraft configuration or for instance upon detection of power failure on any point of the network. If an alternative path is not available, the OBC shall be able to isolate the faulty node and all the others nodes connected downstream. 
Module should be able to act as a thermal relay for other modules through their interconnectors
"""

genRequirements = """
The MOSAR spacecraft shall support the launch of a GEO telecommunication satellite with an initial payload capacity during Phase 1.
The modular spacecraft shall be designed with key concepts of modularity and scalability to meet the mission objective.
During Phase 2, the MOSAR spacecraft shall be capable of increasing the payload capacity of the telecommunication satellite.
The MOSAR spacecraft shall be able to perform upgrades to the payload of the telecommunication satellite during Phase 2.
The modular spacecraft shall provide support for the addition of hosted payloads during Phase 2.
In Phase 3, the MOSAR spacecraft shall be able to replace a failed battery of the telecommunication satellite.
The modular spacecraft shall facilitate the addition of a deorbiting propulsion kit to the telecommunication satellite during Phase 3.
The MOSAR spacecraft shall review, extend, and integrate common robotic building blocks such as ESROCOS, ERGO, InFuse software building blocks, I3DS perception suite, and SIROM standard interface.
The modular spacecraft shall incorporate a repositionable walking manipulator that enables cost-effective actuation on a wide workspace without escalating in size and performance.
The MOSAR spacecraft shall elaborate on a concept for modular spacecraft design, identifying key design choices and providing recommendations for the development of standards for future modular space vehicles.
"""

genRequirements = """
The MOSAR spacecraft shall be capable of upgrading, reconfiguring, and repairing an operational GEO telecommunication satellite.
The initial telecommunication payload capacity of the satellite shall be integrated and tested on the ground.
The satellite's design shall incorporate modular and scalable concepts to meet the mission objective.
The MOSAR spacecraft shall be able to launch the satellite with its initial capacity during Phase 1.
The capacity of the satellite shall be increased during Phase 2 of the mission.
The MOSAR spacecraft shall be able to upgrade the payload of the satellite during Phase 2.
The spacecraft shall have the capability to add a hosted payload to the satellite during Phase 2.
The failed battery of the satellite shall be replaced during Phase 3.
The MOSAR spacecraft shall be equipped with a deorbiting propulsion kit for the satellite during Phase 3.
The MOSAR project shall review, extend, and integrate common robotic building blocks such as ESROCOS, ERGO, InFuse software building blocks, I3DS perception suite, and SIROM standard interface.
The project shall develop a repositionable walking manipulator for the spacecraft.
The walking manipulator shall provide a cost-effective solution for actuation on a wide workspace without escalating size and performance.
The MOSAR spacecraft shall incorporate a concept for a modular spacecraft design.
The design choices for the modular spacecraft shall be identified and documented.
The spacecraft shall adhere to the recommended standards for the design and operation of future modular space vehicles.
The modular spacecraft shall implement a physical interface for docking and/or berthing of the servicer satellite.
The modular spacecraft shall remain coupled to the servicer spacecraft without any time limitations.
The modular spacecraft shall be capable of communicating with the servicer spacecraft.
The spacecraft shall be able to exchange data with the servicer spacecraft during and after rendezvous operations.
The MOSAR project shall demonstrate the essential technologies required for future applications of On-Orbit Servicing and On-Orbit Assembly.
"""

genRequirements = """
The modular spacecraft shall implement a reconfigurable and removable module system that allows for the addition, removal, and exchange of modules from the outside of the satellite.
The modular spacecraft shall have standard interfaces on the outside of the satellite to facilitate in-space connection of additional modules.
The modular spacecraft shall have a propulsion system capable of raising its orbit from a GTO to a GEO position slot.
The modular spacecraft shall be capable of in-orbit tests and commissioning after reaching its GEO position slot.
The modular spacecraft shall be capable of delivering an initial telecommunication capacity, such as high throughput internet connection.
The modular spacecraft shall support the upgrading of payload by removing obsolete technologies and adding new telecommunication capacity.
The modular spacecraft shall support the addition of hosted payload modules, such as a meteorology payload on the Earth pointing panel.
The modular spacecraft shall be compatible with a servicer spacecraft equipped with a robotic arm for capturing, transporting, and assembling modules.
The modular spacecraft shall undergo in-orbit tests for verification of performances after the assembly of new modules.
The modular spacecraft shall support the replacement of failed components, such as batteries and thrusters, to restore nominal operation.
The modular spacecraft shall be compatible with dedicated modules, such as battery modules and propulsion kits, that are launched separately and brought to the satellite for exchange by a servicer spacecraft.
The modular spacecraft shall support the integration and extension of common robotic building blocks and software building blocks for on-orbit servicing and assembly.
The modular spacecraft shall accommodate a repositionable walking manipulator for cost-effective actuation on a wide workspace without size and performance escalation.
The modular spacecraft shall adhere to recommendations for the design and operation of future modular space vehicles, including the identification of key design choices and the development of standards.
"""

genRequirements = """
The modular spacecraft shall support the in-space connection of additional modules through standard interfaces at the outside of the satellite.
The modular spacecraft shall be capable of integrating and testing the satellite payload modules on-ground prior to launch.
The modular spacecraft shall have a scalable design to accommodate future upgrades and additions of modules.
The modular spacecraft shall feature specific modules dedicated to power generation, including solar arrays and power conditioning equipment.
The modular spacecraft shall allow for the removal and storage of obsolete payload modules.
The modular spacecraft shall enable the replacement of obsolete payload modules with upgraded versions.
The modular spacecraft shall support the addition of telecommunication payload modules to increase capacity.
The modular spacecraft shall facilitate the addition of a hosted payload module for meteorology on the Earth pointing panel.
The modular spacecraft shall perform in-orbit tests to verify the performance of added modules.
The modular spacecraft shall integrate a physical interface for docking and/or berthing with a servicer satellite.
The modular spacecraft shall remain coupled to the servicer spacecraft without any time limitations.
The modular spacecraft shall establish communication and data exchange capabilities with the servicer satellite during and after rendezvous operations.
The modular spacecraft shall be equipped with a propulsion system for raising its orbit to reach the GEO position slot.
The modular spacecraft shall have the ability to deliver an initial capacity, such as high throughput internet connection, after in-orbit tests and commissioning.
The modular spacecraft shall support the capture and transportation of dedicated modules by a servicer equipped with a robotic arm.
The modular spacecraft shall facilitate the assembly of captured modules in a specific sequence, including power generation module addition, removal and replacement of payload modules, and addition of telecommunication and hosted payload modules.
The modular spacecraft shall verify the performance of assembled modules through in-orbit tests.
The modular spacecraft shall support the replacement of failed components, such as batteries and thrusters, to ensure nominal operations.
The modular spacecraft shall allow for the addition of a deorbiting propulsion kit for performing specific station-keeping maneuvers.
The modular spacecraft shall enable the exchange of dedicated modules with a servicer in orbit to maintain functionality and performance.
"""

# genRequirements = """
# MOSAR (Modular Spacecraft Repair and Update) is an innovative project aimed at developing a cutting-edge technology for the repair and reconfiguration of modular spacecraft. The project revolves around the use of a robotic manipulator to manipulate and reposition functional modules, enabling the repair and update of spacecraft in orbit.

# The modular spacecraft designed for MOSAR is highly reconfigurable, allowing the integration of new functional modules to introduce additional capabilities and perform new mission tasks. The robotic manipulator plays a crucial role in the process, capable of adding and replacing entire functional modules using their interconnectors.

# To facilitate the efficient planning and execution of repairs and reconfigurations, a dedicated design software is developed. This software enables the creation of robotic-compatible servicing and reconfiguration plans for the modular spacecraft. Additionally, a simulation software is provided to simulate the system and its robotic elements, allowing for accurate testing and validation of the execution plan.

# The modular spacecraft itself assumes high-level control of the robotic manipulator by executing and monitoring the reconfiguration plan at the task level. At the same time, the robotic manipulator ensures low-level control for the precise execution of high-level tasks.

# Monitoring the status of essential parameters of each connected functional module is a vital aspect of MOSAR. The modular spacecraft is equipped with the ability to monitor these parameters, allowing for proactive detection of defects or failures. In the event of a defect, the system is designed to automatically reallocate resources and assign different paths to maintain the spacecraft's functionality.

# The system is resilient to connection failures or power interruptions in defective modules or interconnectors. It can handle tasks seamlessly even under such circumstances, ensuring the continuity of operations.

# MOSAR offers various module options to meet different functional requirements. These options include modules for electrical power supply, data handling systems, heat management functions, propulsion subsystems for station keeping maneuvers, orbit relocation, and de-orbiting, as well as attitude control subsystems for spacecraft reorientation, mission-compatible attitude control, and autonomous search capabilities.

# The interconnectors play a crucial role in MOSAR, allowing modules to connect mechanically to each other or to the spacecraft. Furthermore, modules can act as data and power relays for other modules or the robotic manipulator, even in safe mode, ensuring seamless communication and power distribution within the system.

# The On-Board Computer (OBC) serves as a central control unit, capable of redirecting telecommands to specific modules for spacecraft configuration or in the event of failure detection. If an alternative path is not available, the OBC isolates the faulty node and the downstream connected nodes, ensuring the system's overall integrity.

# Finally, MOSAR incorporates thermal relay capabilities, allowing modules to act as thermal relays for other modules through their interconnectors. This feature ensures efficient heat management and thermal regulation within each module's specific temperature range.

# In summary, MOSAR is an advanced project that revolutionizes modular spacecraft repair and update capabilities. Through the use of robotic manipulation, reconfigurable spacecraft design, and intelligent control systems, MOSAR enables efficient and reliable maintenance and enhancement of spacecraft functionality in space.
# """

# genRequirements = """
# The selection of the MOSAR space mission application has to be done in perspective with the other space mission applications selected for PULSAR and for EROSS:
#  PULSAR space mission will consist in assembling a large telescope at Earth-Sun L2 point using a robotic manipulator, with all the telescope and platform elements packaged in a single launch.
#  EROSS space mission will consist in the in-space servicing of a LEO satellite, with refueling and units replacement, using state-of-the-art robotic arm and equipment.

# Following the analysis of RD2, a mission concept is proposed that exploits at best the benefits of the modular approach, that is realistically feasible in the short/mid-term and that is commercially oriented towards the reduction of costs and the maximization of profit.

# The proposed MOSAR space mission application consists in upgrading, reconfiguring and repairing an operational GEO telecommunication satellite.

# The satellite, in its original configuration, will have an initial telecommunication payload capacity and will be assembled and tested on-ground, but it will feature key design concepts to meet the mission objective:
#  Modular design:
# The satellite original configuration will be based on the conventional all-integrated platform, but will feature some specific modules, removable from the outside of the satellite, dedicated to power generation (solar array + power conditioning) and payloads.
#  Scalable design:
# The satellite original configuration will allow in-space connection of additional modules through standard interfaces at the outside of the satellite. 

# The mission is divided into 3 different phases:
#  Phase 1: launch of satellite with initial capacity
# The satellite is assembled and tested on-ground and is launched fully integrated into a GTO. The satellite then uses its own propulsion system to raise its orbit to reach its GEO position slot. After in-orbit tests and commissioning, the satellite is capable to deliver an initial capacity (e.g. high throughput internet connection).
#  Phase 2: capacity increase + upgrade of payload + addition of hosted payload
# After several years in-orbit (approximately 5 years), there is a need coming from the market to upgrade the payload (removal of obsolete technologies) and to add telecommunication capacity to the existing satellite, while also adding an hosted payload for meteorology on the Earth pointing panel to increase financial revenues and profitability.
# Dedicated modules (power generation module, payload modules, hosted payload module) will be manufactured, tested on-ground and launched into GTO (can be a co-passenger with another GEO
# satellite). A servicer equipped with a robotic arm and positioned near the GTO injection point, will then capture the modules, bring them to the satellite operational orbit (i.e. perform an orbit raising and
# insertion into GEO slot of its client) where it will assemble them with the following sequence:
# o Addition of power generation module and in-orbit tests for verification of performances
# o Removal and storage of obsolete payload modules
# o Replacement of obsolete payload modules and in-orbit tests for verification of performances
# o Addition of telecommunication payload modules and in-orbit tests for verification of performances
# o Addition of hosted payload module and in-orbit tests for verification of performances
#  Phase 3: replacement of failed battery + addition of deorbiting propulsion kit
# After additional years of operations, failure of parts subjected to ageing (e.g. battery, thrusters) occurred preventing the satellite from operating nominally and performing specific station keeping maneuvers (e.g. E/W or N/S).

# Dedicated modules (battery module, propulsion kit) are manufactured, tested on-ground and launched as co-passenger to another GTO mission. As for Phase 2, a servicer will capture and bring them to the satellite operational orbit and perform the modules exchange.

# This mission concept is proposed as an example, to guide the development of the demonstrator. However it should not limit in any way the applicability of MOSAR to any other kind of mission. 

# MOSAR is a project aiming at demonstrating a set of key technologies that are considered essential for the development of future applications of On-Orbit Servicing and On-Orbit Assembly. The objectives of MOSAR include (AD3): 
#  Review, extension and integration of common robotic building blocks: ESROCOS, ERGO and InFuse software building blocks; I3DS perception suite and SIROM standard interface.
#  Development of a repositionable walking manipulator, enabling a cost-effective solution for actuation on a wide workspace without escalation of size and performance of the robot.
#  Elaboration of a concept for modular spacecraft: identifying key design choices and highlighting recommendations for development of standards for design and operation of future modular space vehicles.

# The first two objectives should be generic and independent from any specific mission, as the final purpose is to develop a standard that is unique and re-usable across different missions. As for the third objective, the applicability of the modular approach to different missions is discussed in RD2, highlighting the main advantages that modularity would bring to specific applications and the main design and operation requirement that would need to be fulfilled.
# """

origRequirements = """
As a Data user, I want to have the 12-19-2017 deletions processed.
As a UI designer, I want to redesign the Resources page, so that it matches the new Broker design styles.
As a UI designer, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX.
As a UI designer, I want to move on to round 2 of DABS or FABS landing page edits, so that I can get approvals from leadership.
As a UI designer, I want to move on to round 2 of Homepage edits, so that I can get approvals from leadership.
As a UI designer, I want to move on to round 3 of the Help page edits, so that I can get approvals from leadership.
As a Developer , I want to be able to log better, so that I can troubleshoot issues with particular submissions and functions.
As a Developer, I want to add the updates on a FABS submission to be modified when the publishStatus changes, so that I know when the status of the submission has changed.
As a DevOps engineer, I want New Relic to provide useful data across all applications.
As a UI designer,  I want to move on to round 2 of the Help page edits, so that I can get approvals from leadership.
As a UI designer, I want to move on to round 2 of Homepage edits, so that I can get approvals from leadership.
As a Broker user, I want to Upload and Validate the error message to have accurate text.
As a Broker user, I want the D1 file generation to be synced with the FPDS data load, so that I don't have to regenerate a file if no data has been updated.
As a Website user, I want to access published FABS files, so that I can see the new files as they come in.
As an owner, I want to be sure that USAspending only send grant records to my system.
As a Developer, I want to update the Broker validation rule table to account for the rule updates in DB-2213.
As a Developer, I want to add the GTAS window data to the database, so that I can ensure the site is locked down during the GTAS submission period.
As a Developer, I want D Files generation requests to be managed and cached, so that duplicate requests do not cause performance issues.
As a user, I want to access the raw agency published files from FABS via USAspending.
As an Agency user, I want to be able to include a large number of flexfields without performance impact.
As a Broker user, I want  to help create content mockups, so that I can submit my data efficiently.
As a UI designer, I want to track the issues that come up in Tech Thursday, so that I know what to test and what want s to be fixed.
As an Owner, I want to create a user testing summary from the UI SME, so that I can know what UI improvements we will follow through on.
As a UI designer, I want to begin user testing, so that I can validate stakeholder UI improvement requests.
As a UI designer, I want to schedule user testing, so that I can give the testers advanced notice to ensure buy-in.
As an Owner, I want to design a schedule from the UI SME, so that I know the potential timeline of the UI improvements wanted.
As an Owner, I want to design an audit from the UI SME, so that I know the potential scope of the UI improvements want ed.
As a Developer, I want to prevent users from double publishing FABS submissions after refreshing, so that there are no duplicates.
As an data user, I want to receive updates to FABS records.
As an Agency user, I want to be able to include a large number of flexfields without performance impact.
As a Developer , I want to update the FABS sample file to remove FundingAgencyCode after FABS is updated to no longer require the header.
As an agency user, I want to ensure that deleted FSRS records are not included in submissions.
As a website user, I want to see updated financial assistance data daily.
As a user, I want the publish button in FABS to deactivate after I click it while the derivations are happening, so that I cannot click it multiple times for the same submission.
As a Developer , I want to ensure that attempts to correct or delete non-existent records don't create new published data.
As an Owner, I want to reset the environment to only take Staging MAX permissions, so that I can ensure that the FABS testers no longer have access.
As a user, I want the flexfields in my submission file to appear in the warning and error files when the only error is a missing required element.
As a user, I want to have accurate and complete data related to PPoPCode and PPoPCongressionalDistrict.
As an agency user, I want the FABS validation rules to accept zero and blank for loan records.
As an Agency user, I want FABS deployed into production, so I can submit my Financial Assistance data.
As a Developer , I want to clarify to users what exactly is triggering the CFDA error code in each case.
As an agency user, I want to be confident that the data coming from SAM is complete.
As a Developer , I want my domain models to be indexed properly, so that I can get validation results back in a reasonable amount of time.
As an agency user, I want the FABS validation rules to accept zero and blank for non-loan records.
As a broker team member, I want to make some updates to the SQL codes for clarity.
As an agency user, I want to have all derived data elements derived properly.
As a broker team member, I want to add the 00***** and 00FORGN PPoPCode cases to the derivation logic.
As a data user, I want to see the office names derived from office codes, so that I can have appropriate context for understanding them.
As a broker user, I want the historical FABS loader to derive fields, so that my agency codes are correct in the PublishedAwardFinancialAssistance table.
As a broker team member, I want to ensure the Broker resources, validations, and P&P pages are updated appropriately for the launch of FABS and DAIMS v1.1.
As a Developer, I want the data loaded from historical FABS to include the FREC derivations, so that I can have consistent FREC data for USASpending.gov.
As a user, I don't want to see NASA grants displayed as contracts.
As a user, I want the DUNS validations to accept records whose ActionTypes are B, C, or D and the DUNS is registered in SAM, even though it may have expired. 
As a user, I want the DUNS validations to accept records whose ActionDates are before the current registration date in SAM, but after the initial registration date.
As a broker team member, I want to derive FundingAgencyCode, so that the data quality and completeness improves.
As an agency user, I want the maximum length allowed for LegalEntityAddressLine3 to match Schema v1.1.
As an agency user, I want to use the schema v1.1 headers in my FABS file.
As a agency user, I want to map the FederalActionObligation properly to the Atom Feed.
As a Broker user, I want to have PPoPZIP+4 work the same as the Legal Entity ZIP validations.
As a FABS user, I want to link the SAMPLE FILE on the "What you want  to submit" dialog to point to the correct file, so that I have an accurate reference for my agency submissions.
As an Agency user, I want FPDS data to be up-to-date daily.
As a user, I want to access the raw agency published files from FABS via USAspending.
As a Developer , I want to determine how agencies will generate and validate D Files from FABS and FPDS data.
As a user, I want to generate and validate D Files from FABS and FPDS data.
As an Agency user, I want the header information box to show updated date AND time, so that I know when it was updated.
As an Agency user, I want to receive a more helpful file-level error when I upload a file with the wrong extension.
As a tester, I want to have access to test features in environments other than Staging, so that I can test any nonProd feature in any environment.
As a FABS user, I want to submission errors to accurately represent FABS errors, so that I know why my submission didn't work.
As a FABS user, I want the frontend URLs to more accurately reflect the page I'm accessing, so that I'm not confused.
As an Agency user, I want all historical Financial Assistance data loaded for FABS go-live.
As a Developer , I want the historical FPDS data loader to include both extracted historical data and FPDS feed data.
As an Agency user, I want historical FPDS data loaded.
As an Agency user, I want to accurately see who created a submission, so that I'm not confused about who last updated a submission.
As an agency user, I want to get File F in the correct format.
As an Agency user, I want to better understand my file-level errors.
As a Developer , I want to provide FABS groups that function under the FREC paradigm.
As a tester, I want to ensure that FABS is deriving fields properly through a robust test file plus a follow up check.
As an owner, I only want zero-padded fields, so that I can justify padding.
As a Broker user, I want to submit records for individual recipients without receiving a DUNS error.
As a user, I want more information about how many rows will be published prior to deciding whether to publish.
As a Developer, I want to prevent duplicate transactions from being published and deal with the time gap between validation and the publishing decision.
As a FABS user, I want to submit a citywide as a PPoPZIP and pass validations.
As a Broker user, I want to have updated error codes that accurately reflect the logic and provide enough information, so that I can fix my submission.
As an agency user, I want to leave off the last 4 digits of the ZIP without an error, so that I can complete my submissions.
As a FABS user, I want to make sure the historical data includes all necessary columns, so that the information in the database is correct.
As a data user, I want to access two additional fields from the FPDS data pull.
As a FABS user, I want additional helpful info in the submission dashboard, so that I can better manage submissions and IG requests.
As a FABS user, I want to download the uploaded FABS file, so that I can get the uploaded file.
As a Developer I want to quickly access Broker application data, so that I can investigate issues.
As a Developer , I want to determine the best way to load historical FPDS data, so that I can load all FPDS data since 2007.
As a FABS user, I want the language on FABS pages to be appropriate for me, so that I am not confused.
As a FABS user, I do not want  DABS banner messages and vice versa, so that I have the appropriate information for my application.
As a FABS user, I want to have read-only access to DABS, so that I can view DABS pages without wanting two sets of permissions.
As a FABS user, I want to have my validations run in a reasonable amount of time.
As a FABS user, I want to see correct status labels on the Submission Dashboard, so that I can quickly see my submission history.
As an agency user, I want to know when the submission periods start and end, so that I know when the submission starts and ends.
As an agency user, I want a landing page to navigate to either FABS or DABS pages, so that I can access both sides of the site.
As an agency user, I want to submit my data elements surrounded by quotation marks, so that Excel won't strip off leading and trailing zeroes.
"""

genRequirements = """
As a UI designer, I want to track the progress of my design edits on the DABS or FABS landing page so that I can get approvals from leadership efficiently.
As a UI designer, I want to track the progress of my design edits on the Homepage so that I can get approvals from leadership efficiently.
As a UI designer, I want to track the progress of my design edits on the Help page so that I can get approvals from leadership efficiently.
As a UI designer, I want an approval workflow in the application to facilitate design approvals from leadership.
As a UI designer, I want to redesign the Resources page to match the new Broker design styles.
As a UI designer, I want to report the results of user testing to the agencies to keep them informed about their contributions to improving the UX of the Broker.
As a UI designer, I want to track and document issues identified during Tech Thursday sessions.
As a UI designer, I want to conduct user testing to validate stakeholder UI improvement requests.
"""
distance = compute_jaro_winkler_distance(origRequirements, genRequirements)
print(f"Jaro-Winkler Distance: {distance}")

similarity = compute_cosine_similarity(origRequirements, genRequirements)
print(f"Cosine Similarity: {similarity}")

jaccard_similarity = compute_jaccard_similarity(origRequirements, genRequirements)
print(f"Jaccard Similarity: {jaccard_similarity}")

euclidean_distance = compute_euclidean_distance(origRequirements, genRequirements)
print(f"Euclidean Distance: {euclidean_distance}")