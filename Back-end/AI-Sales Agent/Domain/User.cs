
using Microsoft.AspNetCore.Identity;
using System.Collections.ObjectModel;

namespace AI_Sales_Agent.Domain
{
    public class User : IdentityUser<Guid>
    {
        public string FirstName { get; set; } = string.Empty;
        public string LastName { get; set; } = string.Empty;

        public DateTime? LastLogin {  get; set; } 

        //plans
        public Guid planId { get; set; }
        public Plan? Plan { get; set; }

        //Subscription
        public Subscription? subscription { get; set; }

        //store
        public ICollection<Store> stores { get; set; } = new List<Store>();
    }
}
