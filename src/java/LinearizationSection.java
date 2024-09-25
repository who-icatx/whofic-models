package None;

import java.util.List;
import lombok.*;






/**
  Description of an entity's set of linearization specifications 
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class LinearizationSection extends LiniearizationEntity {

  private String whoficEntityIri;
  private List<LinearizationSpecification> linearizationSpecifications;
  private LinearizationResiduals linearizationResiduals;

}