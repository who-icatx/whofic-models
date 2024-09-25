package None;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class ScaleCustomization extends ContentModelEntity {

  private String postcoordinationAxis;
  private List<PostcoordinationScaleValue> postcoordinationScaleValues;

}