package None;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class PostcoordinationSpecification extends ContentModelEntity {

  private String linearizationView;
  private AllowedRequiredPostcoordinationAxes postcoordinationAxes;

}