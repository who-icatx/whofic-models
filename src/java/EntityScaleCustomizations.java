package None;

import java.util.List;
import lombok.*;






/**
  An entity that holds the Postcoordination scale customization information 
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class EntityScaleCustomizations extends ContentModelEntity {

  private String whoficEntityIri;
  private List<ScaleCustomization> scaleCustomizations;

}