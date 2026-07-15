using AI_Sales_Agent.Domain;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace AI_Sales_Agent.Data
{
    public class ApplicationDbContext : IdentityDbContext<User, IdentityRole<Guid>, Guid>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Store> Stores => Set<Store>();
        public DbSet<StoreIntegrations> StoreIntegrations => Set<StoreIntegrations>();
        public DbSet<Subscription> Subscriptions => Set<Subscription>();
        public DbSet<Plan> Plans => Set<Plan>();
        public DbSet<Feature> Features => Set<Feature>();
        public DbSet<PlanFeature> PlanFeatures => Set<PlanFeature>();
        public DbSet<UserStorePermission> UserStorePermissions => Set<UserStorePermission>();

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<PlanFeature>()
                .HasKey(planFeature => new { planFeature.PlanId, planFeature.FeatureId });

            modelBuilder.Entity<PlanFeature>()
                .HasOne(planFeature => planFeature.Plan)
                .WithMany(plan => plan.PlanFeatures)
                .HasForeignKey(planFeature => planFeature.PlanId);

            modelBuilder.Entity<PlanFeature>()
                .HasOne(planFeature => planFeature.Feature)
                .WithMany(feature => feature.PlanFeatures)
                .HasForeignKey(planFeature => planFeature.FeatureId);

            modelBuilder.Entity<UserStorePermission>()
                .HasKey(permission => new { permission.UserId, permission.StoreId });

            modelBuilder.Entity<UserStorePermission>()
                .HasOne(permission => permission.User)
                .WithMany(user => user.StorePermissions)
                .HasForeignKey(permission => permission.UserId)
                .OnDelete(DeleteBehavior.NoAction);

            modelBuilder.Entity<UserStorePermission>()
                .HasOne(permission => permission.Store)
                .WithMany(store => store.UserPermissions)
                .HasForeignKey(permission => permission.StoreId)
                .OnDelete(DeleteBehavior.NoAction);

            modelBuilder.Entity<Store>()
                .HasOne(store => store.User)
                .WithMany(user => user.Stores)
                .HasForeignKey(store => store.UserId);

            modelBuilder.Entity<StoreIntegrations>()
                .HasOne(integration => integration.Store)
                .WithMany(store => store.Integrations)
                .HasForeignKey(integration => integration.StoreId);

            modelBuilder.Entity<Subscription>()
                .HasOne(subscription => subscription.User)
                .WithOne(user => user.Subscription)
                .HasForeignKey<Subscription>(subscription => subscription.UserId);

            modelBuilder.Entity<Subscription>()
                .HasOne(subscription => subscription.Plan)
                .WithMany(plan => plan.Subscriptions)
                .HasForeignKey(subscription => subscription.PlanId);
        }
    }
}
