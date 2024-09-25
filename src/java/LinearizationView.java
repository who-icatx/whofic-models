package None;

import java.util.List;
import lombok.*;






/**
  The schema of a linearization
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class LinearizationView extends ContentModelEntity {

  private String id;
  private String description;
  private String rootId;
  private String linearizationMode;
  private String coreLinId;
  private String sortingCode;
  private String defaultIsIncluded;
  private String defaultIsGrouping;
  private String defaultIsAuxiliaryAxisChild;

}