 # Yet Another Request Validator - Flask
 
 Yarv allows you to validate flask requests by adding decorators 
 on controllers and passing simple dict based schema to validate 
 against. As it is build upon
 [validators](https://github.com/kvesteri/validators)
 is already comes with a number of pre-defined validations. It 
 allows defining custom validation methods.
 
 ## Features
 - Supports nested schema.
 - Allows addition of custom validators at runtime.
 - Runs on top of [validators](https://github.com/kvesteri/validators) 
 package, so we can use methods defined in `validators` package
 as they are.
 - Allows for passing custom params to each validator, defined in
 the schema which can be positional params, named params or no 
 params.
 
 ## Examples
 WIP
 