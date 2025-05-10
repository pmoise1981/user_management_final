@staticmethod
async def create_invite(
    db: AsyncSession,
    invite_data: InviteCreate,
    inviter: User,
    settings: Settings = Settings()
) -> Invite:
    token = generate_token()
    qr_content = f"{settings.invite_redirect_base_url}/{token}"

    qr_code_filename = f"invite_{inviter.id}_{token}.png"
    qr_code_path = os.path.join(settings.qr_code_dir, qr_code_filename)
    
    # Step 1: Generate the QR code locally
    generate_qr_code(qr_content, qr_code_path)

    # Step 2: Upload the QR code to MinIO
    from app.utils.minio_uploader import upload_qr_code_to_minio
    qr_code_url = upload_qr_code_to_minio(qr_code_path, qr_code_filename)

    # Step 3: Save the invite record in DB with hosted URL
    invite = Invite(
        email=invite_data.email,
        token=token,
        qr_code_url=qr_code_url,
        inviter_id=inviter.id
    )

    db.add(invite)
    await db.commit()
    await db.refresh(invite)
    return invite

