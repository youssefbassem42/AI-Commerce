namespace AI_Sales_Agent.Domain
{
    public class Store: BaseEntity
    {
        public Guid Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Description { get; set; } = string.Empty;

        public string Platform { get; set; } = string.Empty;

        public string ShopDomain { get; set; } = string.Empty;

        public string Currency { get; set; } = string.Empty;

        public string Language { get; set; } = string.Empty;

        public string Timezone { get; set; } = string.Empty;

        public string Status { get; set; } = string.Empty;

        //User
        public Guid UserId { get; set; }
        public User? User { get; set; }

        //Product

    }
}
