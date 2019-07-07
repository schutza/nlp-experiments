# Purpose

This introduces the concept of an Entity Registry as a software component to provide an abstraction layer over management of Entity Type definitions.  
This module encapsulates the following aspects:

* DSL for definition of custom Named Entity Types
* Lifecycle management of custom Named Entity Types
* Registry of supported Named Entity Types
* Mapping of provided 3rd-party entity types to supported Named Entity Types

## Examples

### Restricted list-based entity type

This entity type enumerates all rooms in a house. Entity candidates are controlled, and restricted to the entries in the list. Values outside of the provided entries are not recognised. Optional synonyms allow the detection of the entity in varying expressions.

```json
{
  "name": "Room",
  "description": "closed set of rooms in a house",
  "mechanism": {
    "type": "list",
    "restricted": true,
    "items": [
      {
        "value": "bathroom",
        "synonyms": [
          "bath", "ensuite"
        ]
      },
      {
        "value": "hall"
      },
      {
        "value": "living room",
        "synonyms": [
          "lounge", "sitting room", "good room", "good good room"
        ]
      }
    ]
  },
}
```

### Open list-based entity type

This entity type provides a number of examples in a list. Entity candidates are not restricted to the provided entries, so recognition of `Microsoft Azure HDInsight` or `IBM InfoSphere` would be possible.

```json
{
  "name": "Big Data Vendors",
  "description": "Companies that play in the big data industry",
  "mechanism": {
    "type":   "list",
    "restricted": false,
    "items": [
      {
        "value": "Cloudera"
      },
      {
        "value": "HortonWorks"
      },
      {
        "value": "Amazon EMR",
        "synonyms": [
          "EMR", "Elastic MapReduce"
        ]
      },
      {
        "value": "MapR",
        "synonyms": [
          "EMR", "Elastic MapReduce"
        ]
      }
    ]
  }
}
```

### Regular Expression Entity Type

This entity type provides a number regular expressions in order to control entities. It is useful for entity candidates where the internal shape is known beforehand.

```json
{
  "name": "Flight Numbers",
  "description": "Recognizes flight numbers across various airlines that adhere to the given regular expression, for example: AA4711, FR0815, AA 1234",
  "mechanism": {
    "type":   "regexp",
    "restricted": false,
    "entries": [
      {
        "value": "[A-Z][A-Z]\\s?[0-9]{4,4}"
      }
    ]
  }
}
```

### Context Pattern Entity Type

This entity type provides a context pattern. It is useful when the surrounding context of candidates is known beforehand, but the internal shape not.

```json
{
  "name": "Book Titles",
  "description": "Recognizes book titles based on their surrounding context, for example: author of the novel |The Catcher in the Rye|., She wrote the best-selling novel |Gone Girl|",
  "mechanism": {
    "type": "context pattern",
    "restricted": false,
    "entries": [
      {
        "value": "author of the novel |.*|."
      },
      {
        "value": "wrote the best-selling novel |.*|."
      }
    ]
  }
}
```

### Provided Entity Type

Provided entity types (e.g. `location`, `datetime`, etc.), that are supported by 3rd-party providers such as Snips, LUIS, IBM Watson etc., need to be channeled through this framework, and mapped to the corresponding defined entity types.

## Adapters to 3rd-party Entity Recognizers

Today, Dialog Engine and NLU Service only support 4 builtin slot types / entity types:

* builtin.datetime
* builtin.currency
* builtin.X
* builtin.Y

The prefix `builtin` in this case refers to the implementation provided by Snips. Special effort should be made to encapsulate this reference properly.

### Benefits of an Entity Type Registry

#### Encapsulation

Genesys NLU must control which Entity Types it provides. That does not mean Genesys NLU has to implement Entity Types already provided by other 3rd-parties, such as `location`, `currency`, etc.
But Genesys NLU has to provide its own abstraction layer to those. This also enables leveraging multiple 3rd-party provider interchangeably.

#### Re-usability of Entity Types across Domains

Some entity types are specific to a particular domain (e.g. `Flight Numbers`), some have scope over multiple domains (e.g. `Bank Account Numbers`).
Today, an Entity Type is defined within the scope of a Domain, and re-use across domains is not possible out-of-the-box. The Entity Type definition would have to be duplicated in order to achieve that.
With an abstraction layer over entities as first-class citizens, re-use would become possible.

#### Adaptability of 3rd-party Entity Types

As mentioned above, encapsulation would allow 3rd-party Entity Types to be leveraged under a common schema.
With an appropriate layer of abstraction in place, further benefits would include a more granular control of how 3rd-party entities are mapped into slots.
For example, a case has been made to distinguish between *Date* and *Time* where appropriate, instead of utilizing a *DateTime* entity.
Entity Types could be implemented according to business requirements, and adaptation of provided Entity Types would happen in that abstraction layer.

Example:

* Detected Intent: Order Inquiry
* Slot to Fill: Date
* Dialog
  * Bot: When did you make the order?
  * Customer: Last Friday.
* Genesys NLU: Last Friday/DateTime -> `2019-05-31T00:00:00Z`
  * This resolution to DateTime is too granular, and Dialog would have to make further adjustments to *coarsen* the resolved value to `2019-05-31`

In absence of a different temporal Entity Type, NLU quickly reaches its limits. If there were separate additional Entity Types of `Date` and `Time` to start with, many use-cases would be spared cumbersome post-processing of NLU output at the Dialog level.

## Use Cases

### Date/Time without constraints

Given NLU Context with no constraint\
And customer input is: "On Friday."\
When NLU performs,\
Then an Entity of type Date is returned,\
With Value: Friday/next-Friday-from-today.

### Date/Time with constraint: past

Given NLU Context with constraint of Date/past\
And customer input is: "I was here yesterday"\
When NLU performs,\
Then an Entity of type Date is returned,\
With Value: Friday/previous-Friday-from-today.
