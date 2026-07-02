from django.contrib import admin
from .models import (
    BannerRegions,  Banners,          Costs,         CurrencyConfigOptions, CurrencyConfigs, 
    FailedJobs,     Files,            FilesTags,     Migrations,            Parameters, 
    PasswordResets, Payments,         People,        PersonalAccessTokens,  Phases,
    ProjectCosts,   ProjectItems,     ProjectPeople, ProjectPhaseItems,     ProjectPhases, 
    ProjectTaxes,   ProjectTemplates, Projects,      Tags,                  Taxes, 
    Users
    )

#### APENAS O DANIEL PODE ESSE ARQUIVO // FEV-12
@admin.register(BannerRegions)
class BannerRegionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'state', 'banner', 'created_at', 'updated_at')
    search_fields = ('state',)
    list_filter   = ('created_at', 'updated_at')

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'file_path', 'url_path', 'expiration_date', 'banner_type')
    search_fields = ('name',)
    list_filter   = ('expiration_date', 'banner_type')

@admin.register(Costs)
class CostsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'description', 'value', 'user', 'created_at', 'updated_at')
    search_fields = ('description',)
    list_filter   = ('created_at', 'updated_at')

@admin.register(CurrencyConfigOptions)
class CurrencyConfigOptionsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'currency_code', 'created_at', 'updated_at')
    search_fields = ('currency_code',)
    list_filter   = ('created_at', 'updated_at')

@admin.register(CurrencyConfigs)
class CurrencyConfigsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'currency_config_option', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter   = ('created_at', 'updated_at')

@admin.register(FailedJobs)
class FailedJobsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'uuid', 'failed_at')
    search_fields = ('uuid',)
    list_filter   = ('failed_at',)

@admin.register(Files)
class FilesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'description', 'file_path', 'sharing_type', 'url_path', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter   = ('sharing_type', 'created_at', 'updated_at')

@admin.register(FilesTags)
class FilesTagsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'file', 'tag', 'created_at', 'updated_at')
    search_fields = ('file__name', 'tag__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(Migrations)
class MigrationsAdmin(admin.ModelAdmin):
    list_display  = ('migration', 'batch')
    search_fields = ('migration',)

@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
    list_display  = ('email', 'phone')
    search_fields = ('email', 'phone')

@admin.register(PasswordResets)
class PasswordResetsAdmin(admin.ModelAdmin):
    list_display  = ('email', 'token', 'created_at')
    search_fields = ('email', 'token')
    list_filter   = ('created_at',)

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'eduzz_customer_email', 'eduzz_coupon_code', 'eduzz_contract_plan', 'created_at', 'updated_at')
    search_fields = ('user__name', 'eduzz_customer_email', 'eduzz_coupon_code')
    list_filter   = ('created_at', 'updated_at', 'eduzz_contract_status')

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'position', 'value', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'position', 'user__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(PersonalAccessTokens)
class PersonalAccessTokensAdmin(admin.ModelAdmin):
    list_display  = ('id', 'tokenable_type', 'name', 'token', 'last_used_at', 'created_at', 'updated_at')
    search_fields = ('name', 'tokenable_type', 'token')
    list_filter   = ('last_used_at', 'created_at', 'updated_at')

@admin.register(Phases)
class PhasesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'project_template', 'created_at', 'updated_at')
    search_fields = ('name', 'project_template__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectCosts)
class ProjectCostsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project', 'value', 'description', 'created_at', 'updated_at')
    search_fields = ('project__project_name', 'description')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectItems)
class ProjectItemsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'phase', 'created_at', 'updated_at')
    search_fields = ('name', 'phase__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectPeople)
class ProjectPeopleAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project', 'person', 'value', 'created_at', 'updated_at')
    search_fields = ('project__project_name', 'person__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectPhaseItems)
class ProjectPhaseItemsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project_phase', 'name', 'time', 'value', 'person', 'created_at', 'updated_at')
    search_fields = ('name', 'project_phase__name', 'person__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectPhases)
class ProjectPhasesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project', 'name', 'order', 'created_at', 'updated_at')
    search_fields = ('project__project_name', 'name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectTaxes)
class ProjectTaxesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project', 'tax', 'value', 'created_at', 'updated_at')
    search_fields = ('project__project_name', 'tax__description')
    list_filter   = ('created_at', 'updated_at')

@admin.register(ProjectTemplates)
class ProjectTemplatesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'type_id', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'project_name', 'customer_name', 'city', 'state', 'user', 'created_at', 'updated_at', 'is_sold', 'is_finished')
    search_fields = ('project_name', 'customer_name', 'city', 'state', 'user__name')
    list_filter   = ('created_at', 'updated_at', 'is_sold', 'is_finished')

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter   = ('created_at', 'updated_at')

@admin.register(Taxes)
class TaxesAdmin(admin.ModelAdmin):
    list_display  = ('id', 'description', 'rate', 'user', 'created_at', 'updated_at')
    search_fields = ('description', 'user__name')
    list_filter   = ('created_at', 'updated_at')

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'email', 'is_admin', 'is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'email')
    list_filter   = ('is_admin', 'is_active', 'created_at', 'updated_at')