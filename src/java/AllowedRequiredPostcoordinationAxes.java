package None;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class AllowedRequiredPostcoordinationAxes extends ContentModelEntity {

  private List<String> requiredAxes;
  private List<String> allowedAxes;

}