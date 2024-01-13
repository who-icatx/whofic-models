"""
Global variables
"""
_defaultDirectory="/Users/tu/Documents/Dropbox/WHO (1)/ContentModelOWL2/model/"
_initialKBFile = "/Users/tu/Documents/Dropbox/WHO (1)/ContentModelOWL2/model/EmptyICDContent.pprj"

_icdLabelPropRef = kb.getOWLDatatypeProperty("http://who.int/icd#label")
_labelProp = "http://www.w3.org/2000/01/rdf-schema#label"
_owlRoot = "http://www.w3.org/2002/07/owl#Thing"
_protegeOWLDir = "/Applications/Protege_3.5/plugins/edu.stanford.smi.protegex.owl"
_savedKBFile = _defaultDirectory + "ICDCirulatorySubset.owl"
_skosAltLabel = "http://www.w3.org/2004/02/skos/core#altLabel"
_sourceNamespace = "http://who.int/icd#"
_sourceRDFSLabelSlot = kb.getRDFProperty(_labelProp)
_systemSubclassOfRef = kb.getRDFProperty("http://www.w3.org/2000/01/rdf-schema#subClassOf")
_systemTypePropRef = kb.getRDFProperty("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
_targetNamespace = "http://who.int/icd#"
_targetUMLSNSProp = "http://who.int/icd#is_prefilled_definition_of"
_titleProp = "http://who.int/icd#icdTitle"
_topReferencedClass = "http://who.int/icd#ReferencedClass"
_umlsNSPropRef=kb.getRDFProperty("http://who.int/icd/umls_definitions#is_prefilled_definition_of")

_icdSections = ["http://who.int/icd#SnomedReferenceSection",
		"http://who.int/icd#TreatmentSection",
		"http://who.int/icd#SpecificConditionSection",
		"http://who.int/icd#DiagnosticCriteriaSection",
		"http://who.int/icd#TermSection",
		"http://who.int/icd#ClinicalDescriptionSection",
		"http://who.int/icd#LinearizationSection",
		"http://who.int/icd#PostcoordinationSection",
		"http://who.int/icd#ICD10NotesAndHintsSection",
		"http://who.int/icd#CausalMechanismAndRiskFactorsSection",
		"http://who.int/icd#DefinitionSection",
		"http://who.int/icd#FunctionalImpactSection"]
_extensionSections = [
		"http://who.int/icd#TermSection",
		"http://who.int/icd#LinearizationSection",
		"http://who.int/icd#DefinitionSection",
		"http://who.int/icd#ValueMetaClass"]
_targetKBICDSectionRefs = []

_icdObjProps = ["http://who.int/icd#icdTitle", "http://who.int/icd#definition", "http://who.int/icd#longDefinition"]
_icdDataProps = ["http://who.int/icd#icdCode", "http://who.int/icd#clamlKind"]
_kbICDObjPropRefs = []
_kbICDDataPropRefs=[]

#import edu.stanford.smi.protegex.owl.model.impl.DefaultOWLNamedClass
booleanInstance = kb.getInstance("http://www.w3.org/2001/XMLSchema#boolean")
stringInstance = kb.getInstance("http://www.w3.org/2001/XMLSchema#string")
intInstance = kb.getInstance("http://www.w3.org/2001/XMLSchema#int")
floatInstance = kb.getInstance("http://www.w3.org/2001/XMLSchema#float")
dateTimeInstance = kb.getInstance("http://www.w3.org/2001/XMLSchema#datetime")


"""
Set up Protege OWL environment
"""
import sys
import urlparse, urllib 
import java.util.ArrayList as ArrayList
from java.io import File

def addToClasspath(dirPath):
    rootDir = File(dirPath)
    if (rootDir.isFile()):
        sys.path = sys.path + [dirPath]
        return
    if (rootDir.isDirectory()):
        sys.path = sys.path + [dirPath]
        # recursively add the subdirectories and the jar files
        for i in rootDir.listFiles():
            if (i.isDirectory()):
                addToClasspath(i.getPath())
            if (i.isFile()):
                if ((i.getName())[-4:] == ".jar"):
                    sys.path = sys.path + [i.getAbsolutePath()]
                
addToClasspath(_protegeOWLDir)

from com.hp.hpl.jena.util import FileUtils
from edu.stanford.smi.protegex.owl import ProtegeOWL
from edu.stanford.smi.protege.model import Project


def initialize():
	for p in _icdObjProps:
		_kbICDObjPropRefs.append(kb.getRDFProperty(p))
	for p in _icdDataProps:
		_kbICDDataPropRefs.append(kb.getRDFProperty(p))
	
