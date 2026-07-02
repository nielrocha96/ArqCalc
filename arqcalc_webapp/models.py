#### APENAS O DANIEL PODE ESSE ARQUIVO 
 
# auto-generated Django model module.
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

#### APENAS O DANIEL PODE ESSE ARQUIVO // FEV-12
class Banners(models.Model):
    id              = models.BigAutoField(primary_key=True)
    name            = models.CharField(max_length=255, blank=True, null=True)
    file_path       = models.CharField(max_length=255, blank=True, null=True)
    url_path        = models.CharField(max_length=255, blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    created_at      = models.DateTimeField(blank=True, null=True)
    updated_at      = models.DateTimeField(blank=True, null=True)
    country_region  = models.IntegerField( blank=True, null=True)
    banner_type     = models.IntegerField()

    class Meta:
        managed  = False
        db_table = 'banners'

class BannerRegions(models.Model):
    id         = models.BigAutoField(primary_key=True)
    state      = models.CharField(max_length=255)
    banner     = models.ForeignKey('Banners', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'banner_regions'

class Costs(models.Model):
    id          = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    value       = models.DecimalField(max_digits=8, decimal_places=2)
    created_at  = models.DateTimeField(blank=True, null=True)
    updated_at  = models.DateTimeField(blank=True, null=True)
    user        = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'costs'

class CurrencyConfigOptions(models.Model):
    id            = models.BigAutoField(primary_key=True)
    currency_code = models.CharField(max_length=255)
    created_at    = models.DateTimeField(blank=True, null=True)
    updated_at    = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'currency_config_options'

class CurrencyConfigs(models.Model):
    id                     = models.BigAutoField(primary_key=True)
    currency_config_option = models.ForeignKey(CurrencyConfigOptions, models.DO_NOTHING)
    user                   = models.ForeignKey('Users', models.DO_NOTHING)
    created_at             = models.DateTimeField(blank=True, null=True)
    updated_at             = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'currency_configs'

class FailedJobs(models.Model):
    id         = models.BigAutoField(primary_key=True)
    uuid       = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue      = models.TextField()
    payload    = models.TextField()
    exception  = models.TextField()
    failed_at  = models.DateTimeField()

    class Meta:
        managed  = False
        db_table = 'failed_jobs'

class Files(models.Model):
    id           = models.BigAutoField(primary_key=True)
    name         = models.CharField(max_length=255, blank=True, null=True)
    description  = models.CharField(max_length=255, blank=True, null=True)
    file_path    = models.CharField(max_length=255, blank=True, null=True)
    created_at   = models.DateTimeField(blank=True, null=True)
    updated_at   = models.DateTimeField(blank=True, null=True)
    sharing_type = models.IntegerField(blank=True, null=True)
    url_path     = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'files'

class FilesTags(models.Model):
    id         = models.BigAutoField(primary_key=True)
    file       = models.ForeignKey(Files, models.DO_NOTHING)
    tag        = models.ForeignKey('Tags', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'files_tags'

class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch     = models.IntegerField()

    class Meta:
        managed  = False
        db_table = 'migrations'

class Parameters(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'parameters'

class PasswordResets(models.Model):
    email      = models.CharField(max_length=255)
    token      = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'password_resets'

class Payments(models.Model):
    id                           = models.BigAutoField(primary_key=True)
    user                         = models.ForeignKey('Users', models.DO_NOTHING)
    
    eduzz_customer_id            = models.IntegerField(blank=True, null=True)
    eduzz_customer_email         = models.CharField(max_length=255, blank=True, null=True)
    eduzz_customer_name          = models.CharField(max_length=255, blank=True, null=True)
    
    eduzz_coupon_code            = models.CharField(max_length=255, blank=True, null=True)
    eduzz_contract_id            = models.IntegerField(blank=True, null=True)
    eduzz_contract_plan          = models.CharField(max_length=255, blank=True, null=True)
    eduzz_contract_startdate     = models.CharField(max_length=255, blank=True, null=True)
    eduzz_contract_status        = models.IntegerField(blank=True, null=True)
    
    eduzz_transaction_id         = models.CharField(max_length=255, blank=True, null=True)
    eduzz_transaction_createdate = models.CharField(max_length=255, blank=True, null=True)
    eduzz_transaction_createtime = models.CharField(max_length=255, blank=True, null=True)
    eduzz_transaction_paid       = models.FloatField(blank=True, null=True)
    eduzz_transaction_paiddate   = models.CharField(max_length=255, blank=True, null=True)
    eduzz_transaction_paidtime   = models.CharField(max_length=255, blank=True, null=True)
    eduzz_transaction_status     = models.IntegerField(blank=True, null=True)
    eduzz_transaction_value      = models.FloatField(blank=True, null=True)
    
    created_at                   = models.DateTimeField(blank=True, null=True)
    updated_at                   = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'payments'

class People(models.Model):
    id         = models.BigAutoField(primary_key=True)
    name       = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    position   = models.CharField(max_length=255)
    value      = models.DecimalField(max_digits=8, decimal_places=2)
    user       = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'people'

class PersonalAccessTokens(models.Model):
    id             = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id   = models.PositiveBigIntegerField()
    name           = models.CharField(max_length=255)
    token          = models.CharField(unique=True, max_length=64)
    abilities      = models.TextField(blank=True, null=True)
    last_used_at   = models.DateTimeField(blank=True, null=True)
    
    created_at     = models.DateTimeField(blank=True, null=True)
    updated_at     = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'personal_access_tokens'

class Phases(models.Model):
    id               = models.BigAutoField(primary_key=True)
    name             = models.CharField(max_length=255)
    created_at       = models.DateTimeField(blank=True, null=True)
    updated_at       = models.DateTimeField(blank=True, null=True)
    project_template = models.ForeignKey('ProjectTemplates', models.DO_NOTHING)

    class Meta:
        managed  = False
        db_table = 'phases'

class ProjectCosts(models.Model):
    id          = models.BigAutoField(primary_key=True)
    project     = models.ForeignKey('Projects', models.DO_NOTHING)
    value       = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    created_at  = models.DateTimeField(blank=True, null=True)
    updated_at  = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'project_costs'

class ProjectItems(models.Model):
    id         = models.BigAutoField(primary_key=True)
    name       = models.CharField(max_length=255, blank=True, null=True)
    phase      = models.ForeignKey(Phases, models.DO_NOTHING, blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'project_items'

class ProjectPeople(models.Model):
    id         = models.BigAutoField(primary_key=True)
    project    = models.ForeignKey('Projects', models.DO_NOTHING)
    person     = models.ForeignKey(People, models.DO_NOTHING)
    value      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'project_people'

class ProjectPhaseItems(models.Model):
    id            = models.BigAutoField(primary_key=True)
    project_phase = models.ForeignKey('ProjectPhases', models.DO_NOTHING)
    time          = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    value         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    person        = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)
    name          = models.CharField(max_length=255, blank=True, null=True)
    
    created_at    = models.DateTimeField(blank=True, null=True)
    updated_at    = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'project_phase_items'

class ProjectPhases(models.Model):
    id         = models.BigAutoField(primary_key=True)
    project    = models.ForeignKey('Projects', models.DO_NOTHING)
    name       = models.CharField(max_length=255, blank=True, null=True)
    order      = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'project_phases'

class ProjectTaxes(models.Model):
    id         = models.BigAutoField(primary_key=True)
    project    = models.ForeignKey('Projects', models.DO_NOTHING)
    tax        = models.ForeignKey('Taxes', models.DO_NOTHING)
    value      = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'project_taxes'

class ProjectTemplates(models.Model):
    id         = models.BigAutoField(primary_key=True)
    name       = models.CharField(max_length=255)
    type_id    = models.IntegerField()
    user       = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'project_templates'

class Projects(models.Model):
    id                     = models.BigAutoField(primary_key=True)
    customer_name          = models.CharField(max_length=255, blank=True, null=True)
    project_name           = models.CharField(max_length=255, blank=True, null=True)
    
    street                 = models.CharField(max_length=255, blank=True, null=True)
    street_number          = models.CharField(max_length=255, blank=True, null=True)
    street_additional      = models.CharField(max_length=255, blank=True, null=True)
    neighborhood           = models.CharField(max_length=255, blank=True, null=True)
    city                   = models.CharField(max_length=255, blank=True, null=True)
    state                  = models.CharField(max_length=255, blank=True, null=True)
    
    size                   = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    project_type           = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_first_project       = models.IntegerField(blank=True, null=True)
    cost_value             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at             = models.DateTimeField(blank=True, null=True)
    updated_at             = models.DateTimeField(blank=True, null=True)
    price_project          = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    comission              = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    project_template_id    = models.PositiveBigIntegerField(blank=True, null=True)
    account_name           = models.CharField(max_length=255, blank=True, null=True)
    classification_project = models.CharField(max_length=255, blank=True, null=True)
    
    is_sold                = models.IntegerField(blank=True, null=True)
    is_finished            = models.IntegerField(blank=True, null=True)
    
    user                   = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    start_date             = models.DateTimeField(blank=True, null=True)
    end_date               = models.DateTimeField(blank=True, null=True)
    is_in_dashboard        = models.IntegerField()

    class Meta:
        managed  = False
        db_table = 'projects'

class Tags(models.Model):
    id         = models.BigAutoField(primary_key=True)
    name       = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'tags'

class Taxes(models.Model):
    id          = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=255)
    rate        = models.DecimalField(max_digits=8, decimal_places=2)
    user        = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    created_at  = models.DateTimeField(blank=True, null=True)
    updated_at  = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'taxes'

class Users(models.Model):
    id                 = models.BigAutoField(primary_key=True)
    name               = models.CharField(max_length=255)
    email              = models.CharField(unique=True, max_length=255)
    email_verified_at  = models.DateTimeField(blank=True, null=True)
    password           = models.CharField(max_length=255)
    remember_token     = models.CharField(max_length=100, blank=True, null=True)
    photo_path         = models.CharField(max_length=255, blank=True, null=True)
    
    is_admin           = models.IntegerField()
    integration_id     = models.IntegerField(blank=True, null=True)
    is_active          = models.IntegerField()
    is_first_access    = models.IntegerField()
    
    cellphone          = models.CharField(max_length=255, blank=True, null=True)
    
    address            = models.CharField(max_length=255, blank=True, null=True)
    address_number     = models.CharField(max_length=255, blank=True, null=True)
    address_country    = models.CharField(max_length=255, blank=True, null=True)
    address_district   = models.CharField(max_length=255, blank=True, null=True)
    address_complement = models.CharField(max_length=255, blank=True, null=True)
    address_city       = models.CharField(max_length=255, blank=True, null=True)
    address_state      = models.CharField(max_length=255, blank=True, null=True)
    address_zip_code   = models.CharField(max_length=255, blank=True, null=True)
    
    show_welcome       = models.IntegerField()
    lock_date          = models.DateField(blank=True, null=True)

    created_at         = models.DateTimeField(blank=True, null=True)
    updated_at         = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed  = False
        db_table = 'users'