package None;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class LinearizationResiduals  {

  private LanguageTerm unspecifiedResidualTitle;
  private LanguageTerm otherSpecifiedResidualTitle;
  private String suppressOtherSpecifiedResiduals;
  private String suppressUnspecifiedResiduals;

}