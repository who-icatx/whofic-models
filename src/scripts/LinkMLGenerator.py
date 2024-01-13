#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#Usage: 

First run the following in Protege 3 script console:

execfile("/Users/tu/workspace/whofic-models/src/scripts/LinkMLGenerator.py")
"""
execfile("/Users/tu/workspace/whofic-models/src/scripts/setup.py")
_defaultDirectory="/Users/tu/workspace/whofic-models"


''' 

Then run the following to generate linkML model files

generateLinkMLModels(topClasses, contentModelFile, cmheaderFile) 
'''

topClasses = [ "ICDSection", "ContentModelEntity"]
contentModelFile = _defaultDirectory+ "/linkMLmodels/generated/contentmodel.yaml"
cmheaderFile= _defaultDirectory+ "/resources/cmheaders.yaml"

## Global variables
gClassSchemaRoot = kb.getOWLNamedClass("http://who.int/icd#ICDSection")
gClassSchemaSubsetName = "class_schema_subset"
gClassSchemaDescription = "A subset of the schema that defines templates for class entities"

"""
There are 3 parts to the WHO-FIC modeling:
1. WHO-FIC Metamodel - Schema of WHO-FIC entities
2. ContentModelEntity - Schema for slot value instances
3. ClassificationEnity - Topleval entities of WHO-FIC classificationsEntitiesFile
Initial schemas (parts 1 and 2) will be generated from Protege 3 models

Subsets of schemas:
  class_schema_subset that correspond to subset of schema for WHO entities
  
Limitations
- See https://github.com/samsontu/iCATX/issues



Algorithm for generating LinkML specification
* First, set up global specifications
* Second generate the class definitions
allProperties = []
For each subclass of topClses:
    pSet = all of the properties "associated" with the subclass
    A property is "associated" with a class if
        1. The class is in the domain of the property
        2. The class has a new restriction 
    allProperties = pSet union allProperties
    for each p in pset
        list p in the definition of class
        


"""

def generateLinkMLModels(topClasses, outputFile, headerFile):
    savedStdout = sys.stdout
    try:
        out = open(outputFile, 'w')
    except IOError:
        out = 0
    if out:
        sys.stdout = out
    try:
        printHeader(headerFile)
        print "classes:\n"
        emittedClasses = set()
        for c in topClasses:
            cls = kb.getCls(_sourceNamespace+c)
            if cls:
                classesInScope = cls.getNamedSubclasses(1)
                classesInScope.add(cls)
                emittedClasses = generateSchema(cls,  classesInScope, emittedClasses)
            else:
                sys.stderr.write( _sourceNamespace+c+" is not a class\n")
        writePropertiesDeclaration()
        writeSubsetsDeclaration()
    except:
        sys.stderr.write("\nException at top level. Not all classes were processed\n")
    finally:
        sys.stdout.flush()
        if out:
            out.close()
            sys.stdout = savedStdout
    savedStdout = sys.stdout

def generateSchema(cls, classesInScope, emittedClasses):
    if cls.isDeprecated():
        return emittedClasses
    if (cls not in emittedClasses):
        writeClass(cls, classesInScope)
        emittedClasses.add(cls)
    subs = cls.getNamedSubclasses()
#     print [s.getLocalName() for s in subs]
    for sub in subs:
        emittedClasses = generateSchema(sub, classesInScope, emittedClasses)
    return emittedClasses


def writeClass(cls, classesInScope):
    print "  "+cls.getLocalName()+":"
    supers = cls.getNamedSuperclasses()
    supersInScope = [super for super in supers if (super in classesInScope) and not super.isDeprecated()]
    if supersInScope:
        print "    is_a: "+supersInScope[0].getLocalName()
        if len(supersInScope) > 1:
            print "    mixins:"
            for c in supersInScope[1:]:
                print "      - "+c.getLocalName()
    labels = cls.getLabels()
    description = ""
    for label in labels:
        description = description + label + " "
    if (description == ""):
        description = cls.getLocalName() 
    print "    description >-\n      Description of "+description
    writePropertiesAtClass(cls)
    #Emit Subset membership
    if ((cls == gClassSchemaRoot) or cls.isSubclassOf(gClassSchemaRoot)):
        print "    in_subset:"
        print "      - "+ gClassSchemaSubsetName
    print ""

def writePropertiesAtClass(cls):
        # Print property information at class
    ps = cls.getUnionDomainProperties()
#     print "***  ps"
#     print ps
    rs = cls.getRestrictions()
    rps = [r.getOnProperty() for r in rs]
#     print "*** rps "
#     print rps
    if rps:
        if ps:
            ps = [p for p in ps] #convert java arraylist to python list
            ps.extend(rps)
            properties = set(ps)
        else:
            properties = rps
    else:
        properties = ps
    print "    slots:"
    for p in properties:
        print "      - "+p.getLocalName()
    #Write slot_usage
        writeSlotUsage(cls, p)

def writeSlotUsage(cls, p):
# Not clear class-specific restrictions are relevant
#     rs = cls.getRestrictions()
#     if rs:
#     	print "***"
#     	print rs
    return 0

def writePropertiesDeclaration():
    print "\nslots:"
    for p in kb.getUserDefinedOWLObjectProperties():
        writePropertyDeclaration(p)
    for p in kb.getUserDefinedOWLDatatypeProperties():
        writePropertyDeclaration(p)
    return 0
    
def writeSubsetsDeclaration():
    print "\nsubsets:"
    print "  "+gClassSchemaSubsetName+":"
    print "    description: "+ gClassSchemaDescription

def getRangeStr(p):
    rangeStr =""
    if p.hasObjectRange():
        ranges = p.getUnionRangeClasses()
        if ranges:
            rangeStrs = [r.getLocalName() for r in ranges]
            first = 1
            for str in rangeStrs:
                if first:
                    rangeStr = str
                    first = 0
                else:
                    rangeStr = rangeStr+", "+str
    else:
        range = p.getRange()
        if range:
            rangeStr = range.getBrowserText()
    return rangeStr
        
def writePropertyDeclaration(p):
    print "  "+p.getLocalName()+":"
    print "    slot_uri: icd:" + p.getLocalName()
    writePropertyParentAndMixIn(p)
    rangeStr = getRangeStr(p)
    if (rangeStr):
        print "    range: "+rangeStr
    # Note that in OWL, one can specify that a property is functional, but not multi-valued
    # maximum/minimum cardinalities is defined at class level (although Protégé frame
    # does have slot max/min cardinality declarations). Return -1 in unknown case.
    if (p.isFunctional()or (p.getMaximumCardinality() == 1)):
        print "    multivalued: false"
    if (p.getMaximumCardinality() > 1):
        print "    multivalued: true"
        print "    maximum_cardinality: "+str(p.getMaximumCardinality())
    if (p.getMinimumCardinality() > 0):
        print "    minimum_cardinality: "+str(p.getMinimumCardinality())

def writePropertyParentAndMixIn(p):
    if (p.getSuperpropertyCount()) > 0:
        superPs = p.getSuperproperties(0)
        #Need to convert to python list; otherwise get exception: java.util.Collections$UnmodifiableRandomAccessList
        pList = [prop for prop in superPs]
        print "    is-a: "+ pList[0].getLocalName()
        if p.getSuperpropertyCount() > 1:
            print "    mixins:"
            for supP in pList[1:]:
                print "      - "+supP.getLocalName()


def printHeader(headerFile):
    file = open(headerFile)
    print(file.read())

"""
def generateNodeShape(cls):
    localName =cls.getLocalName()
    print "icd:%sShape\n\ta sh:NodeShape ;\n\tsh:targetClass icd:%s ;"%((localName, localName))

def closeShape():
    print".\n"

#Generate a string consisting of property shapes
def generatePropertyShapes(cls):
    ps = cls.getUnionDomainProperties()
    rs = cls.getRestrictions()
    rps = [r.getOnProperty() for r in rs]
    rpsNotps = [rp for rp in rps if (not (rp in ps))]
    pShapes = ""
    for p in ps:
        pShapes = genCardinalityConstraints(cls, p, pShapes)
        pShapes = genTypeConstrains(cls, p, pShapes)
    for p in rpsNotps:
        pShapes = genCardinalityConstraints(cls, p, pShapes)
        pShapes = genTypeConstrains(cls, p, pShapes)
    if (pShapes == ""):
        return None
    else:
        return pShapes

def genCardinalityConstraints(cls, p, pShapes):
    localName = p.getLocalName()
    if (p.isFunctional() or maxCardinalityEQ1(cls, p)):
        if (minCardianlityGT0(cls, p)):
            pShapes=pShapes+"\n\tsh:property [\n\t\tsh:path icd:%s ; sh:minCount 1; sh:maxCount 1; ];"%((localName))
        else:
            pShapes=pShapes+"\n\tsh:property [\n\t\tsh:path icd:%s ; sh:maxCount 1; ];"%((localName))
    return pShapes

def minCardianlityGT0(cls, p):
    return cls.getMinCardinality(p) > 0
    
def maxCardinalityEQ1(cls, p):
    return (cls.getMaxCardinality(p) == 1)

def genTypeConstrains(cls, p, pShapes):
    if p.isObjectProperty():
        pShapes = genObjectPropertyConstraints(cls, p, pShapes)
    else:
        pShapes = genDatatypePropertyConstraints(cls, p, pShapes)
    return pShapes

def genObjectPropertyConstraints(cls, p, pShapes):
    allValueFrom = cls.getAllValuesFromOnTypes(p)
    if (allValueFrom):
        #sys.stderr.write("\ngenObjectPropertyConstraints entr: "+cls.getName()+": "+p.getLocalName())
        #print allValueFrom
        #targets = allValueFrom.getOperancds()
        pName=p.getLocalName()
        rName=allValueFrom.getLocalName()
        if (allValueFrom.getName().find("http") > -1): #a named class
            pShapes=pShapes+"\n\tsh:property [\n\t\tsh:path icd:%s ; sh:nodeKind sh:IRI; sh:class icd:%s; ];"%((pName, rName))
        else:
            targets = allValueFrom.getOperands()
            if (targets.size() > 1):
                newShape = "\n\tsh:or ("
                for target in targets:
                    rName = target.getLocalName()
                    newShape = newShape+"\n\t\t[sh:path icd:%s ; sh:nodeKind sh:IRI; sh:class icd:%s;]"%((pName, rName))
                newShape=newShape+");"  
                pShapes=pShapes+newShape  
            else:  
                pShapes=pShapes+"\n*******"+allValueFrom.getName()+"  "+pName
#               rName = allValueFrom.getLocalName()
#               pShapes=pShapes+"\n\tsh:property [\n\t\tsh:path icd:%s ; sh:nodeKind sh:IRI; sh:class icd:%s; ];"%((pName, rName))                  
    return pShapes

def genDatatypePropertyConstraints(cls, p, pShapes):
    allValueFrom = cls.getAllValuesFromOnTypes(p)
    if (allValueFrom):
        pName = p.getLocalName()
        datatype = getDatatype(allValueFrom)
        if (datatype):
            pShapes=pShapes+"\n\tsh:property [\n\t\tsh:path icd:%s ;  sh:datatype xsd:%s ;  ];"%((pName, datatype))
    return pShapes

def getDatatype(resource):
    switcher = {
        stringInstance: "string",
        booleanInstance: "boolean",
        floatInstance: "float",
        intInstance: "integer",
        dateTimeInstance: "datatime"
    }
    return switcher.get(resource, None)
"""
