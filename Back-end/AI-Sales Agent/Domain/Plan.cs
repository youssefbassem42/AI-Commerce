namespace AI_Sales_Agent.Domain
{
    public class Plan: BaseEntity
    {
        public Guid Id { get; set; } = Guid.NewGuid();
        public string PlanName { get; set; } = string.Empty;

        public string PlanDescription { get; set; } = string.Empty;
        public string PlanStatus { get; set; } = string.Empty;

        //user
        public ICollection<User> users { get; set; } = new List<User>();

        //Subscription
        public ICollection<Subscription> subscriptions { get; set; } = new List<Subscription>();

        //Plan Features
        public ICollection<PlanFeature> planFeatures { get; set; } = new List<PlanFeature>();

    }
}
