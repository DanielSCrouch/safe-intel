
- Validate dataset input & output matches input range of Models
- Validate operations within model are supported by Verninet/Venus
- early validation of model to vnnlib via parsing 

- model/(vnnlib/dataset) validator - input spec, output spec, dataset input shapes, model, (vapp)

'darkMode': 'true'

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#cfd1d4', 'primaryBorderColor': '#1c4643', 'secondaryColor': '#1c4643'}}}%%
classDiagram

%%======================================================
%% Evaluation Process Results

class Results{
    %% ToDo: define expected evaluation results
    +List[errors] Errors
}

%%======================================================
%% DataSets

class DataSet{
    +String ID
    +String Name
    -List[~Image~] Images
    -Int ImageCount
    -Int Size
}

DataSet "1" o-- "*" Image: Aggregates

class Image{
    +String ID
    +String FileName
    +String Format
    +Int Width
    +Int Height
    +Int FileSize
    +String FilePath
    +Int Label
}

%%======================================================
%% Classification Parameters

class ClassificationParams{
    %% Classification input annotations
    +String Annotations
}

class ObjectDetectionParams{
    %% Slack applied to object box boundary in pixels
    +List~Int~ Slack
}

class SegmentationParams{
    %% Target value of the model output
    +Int Target
}

class BiasFieldParams{
    %% BiasField input parameters
    +Int Order
    +Bool Additive
    +Bool Multiplicative
}

%%======================================================
%% Output Specs

class OutputSpec{
    %% Defines expected model ouput depending upon ML method
    +~OutputSpecType~ Type
    +~ClassificationParams~ ClassificationParams
    +~ObjectDetectionParams~ ObjectDetectionParams
    +~SegmentationParams~ SegmentationParams
    +List[Int] ModelOutputShape

    +Validate() 
    %% Validate - Check ouput specs are valid
}

class OutputSpecType{
    <<enumeration>>
    Classification
    ObjectDetection
    Segmentation
}

OutputSpec *-- OutputSpecType: Composed
OutputSpec *-- ClassificationParams: Composed
OutputSpec *-- ObjectDetectionParams: Composed
OutputSpec *-- SegmentationParams: Composed

%%======================================================
%% Input Specs

class InputSpec{
    %% Defines input parameters for model evaluation algorithm/process
    +InputSpecType Type
    +Float Epsilon
    +Bool ClipPixels
    +Time Timeout
    +~BiasFieldParams~ BiasFieldParams
    
    +Validate() 
    %% Validate - Check input specs are valid
}

class InputSpecType{
    <<enumeration>>
    Contrast
    WhiteNoise
    Brightness
    BiasFields
}

InputSpec *-- BiasFieldParams: Composed
InputSpec *-- InputSpecType: Composed

%%======================================================
%% Objective

class Objective{
    %% Defines the model-evaluation input and output constraints
    +String ID
    +String Name
    +Shape InputShape
    +Shape OutputShape
    +DataSet DataSet
    +InputSpec InputSpec
    +OutputSpec OutputSpec
    +String FilePath
    +String FileFormat %% default is VNNLib
    +Int FileSize    
}

class Shape{
    %% Defines the number of inputs or outputs to a model
    []int Dimensions
}

Objective *-- Shape: Composed

Objective --> DataSet: Association
Objective --> InputSpec: Association
Objective --> OutputSpec: Association


%%======================================================
%% MLModel

class MLModel{
    +String ID
    +String Name
    +String Type
    +Shape InputShape
    +Shape OutputShape
    +String FilePath
    +String FileFormat %% default is ONNX
    +Int FileSize    
}

MLModel *-- Shape: Composed

%%======================================================
%% Evaluation Process

class EvaluationProcess{
    +String ID
    +String Name
    +Bool Verinet/Venus
    +MLModel Model
    +Obective Objective
    +String Status
    +String CreationTime
    +String StartTime
    +String FinishTime
    +Results Results

    +Validate()
    %% Validate - Check model and object configs are valid
}

EvaluationProcess --> MLModel : Association
EvaluationProcess --> Objective : Association
EvaluationProcess --* Results : Composed
```
