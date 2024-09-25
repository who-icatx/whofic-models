package None;

import java.util.List;
import lombok.*;






/**
  Description of LinearizationSpecification
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class LinearizationSpecification extends LiniearizationEntity {

  private LanguageTerm codingNote;
  private String isGrouping;
  private String isIncludedInLinearization;
  private String linearizationSortingLabel;
  private String isAuxiliaryAxisChild;
  private String linearizationParent;
  private String linearizationView;

}