## [unreleased]

### 📚 Documentation

- *(changelog)* Update CHANGELOG
- *(changelog)* Update CHANGELOG
- *(wiki)* Fix grammar
- *(changelog)* Update CHANGELOG
- *(changelog)* Update CHANGELOG
- *(changelog)* Update CHANGELOG

### ⚙️ Miscellaneous Tasks

- Put all the Github Actions to their right place
- *(release)* Make it manually launchable
## [0.1.0] - 2026-01-28

### 🚀 Features

- *(logger)* Add custom logger
- *(types)* Add the config pydantic model
- *(config)* Initialize config class for future use
- *(types)* Add types for a todo.txt list item
- *(config)* Add _expand_config for expanding tilde and env variables
- *(parser)* Implement the todo.txt parser class
- *(visual)* Add a very primitve grouping method for visualization
- *(types)* Add new configuration options and tabular match for visualization
- *(visual)* Improve grouping and implement table generation method
- *(types)* Reorganize configuration structure and defaults
- *(visual)* Make most part of the table generation customizable
- *(visual)* Add configuration option for box styling
- *(visual)* Add config option for title styling
- *(visual)* Implement support for column styles
- *(types)* Change default title color
- *(visual)* Scatter tables according to the terminal width
- *(app)* Add group title argument for filtered results
- *(grouped)* Add line seperator config option
- *(types)* Add all the alphabet to Priority
- Add Eisenhower matrix view generator and reorganize configuration
- *(eisenhower)* Finalize Eisenhower matrix view
- *(config)* Create config file if not exists
- *(grouped)* Implement a very simple trick for human-readable column titles

### 🐛 Bug Fixes

- *(config)* Remove optionality of class variables
- *(types)* Make TodoItem project and context properties a list
- *(parser)* Ensure all TodoItem properties have a value of some kind
- *(types)* Add TodoItemProperty
- *(types)* Use a valid column default
- *(eisenhower)* Convert RenderableMatrix from TypedDict to dict
- *(eisenhower)* Ensure the title of the panels are valid

### 💼 Other

- *(deps)* Add tomli-w for writing to a toml file

### 🚜 Refactor

- *(config)* Use enum messages instead of string literals for errors
- *(parser)* Reorganize the Parser method object
- *(helpers)* Move property to string transformation function
- Split Visualizer to renderer and GroupedTodoView
- *(visual)* Don't use config directly inside the methods
- *(parser)* Don't use config directly inside the methods
- *(app)* Don't use the columns configuration inside renderer
- *(visual)* Clean grouping methods and rename variables for consistency
- *(visual)* Move grouped view methods to views/grouped
- *(grouped)* Implement a grouped view renderer for mulitple use cases

### 📚 Documentation

- *(wiki)* Add wiki items and the relevant GitHub action
- *(README)* Add a proper README

### ⚙️ Miscellaneous Tasks

- *(app)* Create a testing environment (testing in prod?)
- *(parser)* Rename _todo_items to _todo_list for naming consistency
- Rename GroupedTodoView to GroupedView
- *(types)* Rename TitleStyle as TextStyle since it has common properties
- *(types)* Set default todo_path
- *(types)* Set TextStyle bold value to false by default
- *(pyproject)* Change the description of the project
- *(gitcliff)* Add git-cliff the CHANGELOG curator
- *(release)* Add automatic release builder
