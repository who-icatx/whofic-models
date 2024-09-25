package None;

import java.util.List;
import lombok.*;






/**
  Mapping from a post-coordination axis to a generic scale 
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class PostcoordinationAxisToGenericScale extends ContentModelEntity {

  private String postcoordinationAxis;
  private String genericPostcoordinationScaleTopClass;

}